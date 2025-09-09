import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SignupPage from '@/app/(auth)/signup/page';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/context/authContext';

// Mock the useRouter hook
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

// Mock the useAuth hook
jest.mock('@/app/context/authContext', () => ({
  useAuth: jest.fn(),
}));

describe('SignupPage', () => {
  const mockSignup = jest.fn();
  const mockPush = jest.fn();

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
    (useAuth as jest.Mock).mockReturnValue({ signup: mockSignup });
  });

  it('should render the signup form and its elements', () => {
    render(<SignupPage />);

    expect(screen.getByRole('heading', { name: /Create Account/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter your full name/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter your email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Create a strong password/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Confirm your password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Create Account/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Sign in here/i })).toBeInTheDocument();
  });

  it('should update state when user types into the input fields', () => {
    render(<SignupPage />);

    const nameInput = screen.getByPlaceholderText(/Enter your full name/i);
    const emailInput = screen.getByPlaceholderText(/Enter your email/i);
    const passwordInput = screen.getByPlaceholderText(/Create a strong password/i);

    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'P@ssw0rd123' } });

    expect(nameInput).toHaveValue('John Doe');
    expect(emailInput).toHaveValue('john@example.com');
    expect(passwordInput).toHaveValue('P@ssw0rd123');
  });

  it('should call signup and redirect on successful form submission', async () => {
    render(<SignupPage />);

    // Fill out the form with valid data
    fireEvent.change(screen.getByPlaceholderText(/Enter your full name/i), { target: { value: 'Jane Doe' } });
    fireEvent.change(screen.getByPlaceholderText(/Enter your email/i), { target: { value: 'jane.doe@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/Create a strong password/i), { target: { value: 'ValidP@ss123' } });
    fireEvent.change(screen.getByPlaceholderText(/Confirm your password/i), { target: { value: 'ValidP@ss123' } });
    fireEvent.change(screen.getByRole('combobox', { name: /Account Type/i }), { target: { value: 'seller' } });

    // Mock the signup function to resolve successfully
    mockSignup.mockResolvedValue(undefined);

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Create Account/i }));

    // Wait for the signup function to be called with the correct data
    await waitFor(() => {
      expect(mockSignup).toHaveBeenCalledWith({
        name: 'Jane Doe',
        email: 'jane.doe@example.com',
        password: 'ValidP@ss123',
        role: 'seller',
      });
    });

    // Check for success message and redirection
    await waitFor(() => {
      expect(screen.getByText('Account created successfully! Redirecting to login...')).toBeInTheDocument();
    });

    // Use a short delay in the test to account for the setTimeout in the component logic
    await new Promise(resolve => setTimeout(resolve, 2000));
    expect(mockPush).toHaveBeenCalledWith('/login');
  });

  it('should display an error message if the signup API call fails', async () => {
    render(<SignupPage />);

    // Fill out the form with valid data
    fireEvent.change(screen.getByPlaceholderText(/Enter your full name/i), { target: { value: 'John Smith' } });
    fireEvent.change(screen.getByPlaceholderText(/Enter your email/i), { target: { value: 'john.smith@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/Create a strong password/i), { target: { value: 'ValidP@ss123' } });
    fireEvent.change(screen.getByPlaceholderText(/Confirm your password/i), { target: { value: 'ValidP@ss123' } });

    // Mock a failed signup attempt
    const errorMessage = 'Email already in use';
    mockSignup.mockRejectedValue(new Error(errorMessage));

    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Create Account/i }));

    // Check for the error message
    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    // Ensure no redirection occurred
    expect(mockPush).not.toHaveBeenCalled();
  });
});