// __tests__/LoginPage.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoginPage from '@/app/(auth)/login/page'; // adjust path if needed
import { useAuth } from '@/app/context/authContext';
import { useRouter } from 'next/navigation';

jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}));

jest.mock('@/app/context/authContext', () => ({
  useAuth: jest.fn(),
}));

describe('LoginPage (minimal)', () => {
  const mockLogin = jest.fn();
  const mockPush = jest.fn();
  const mockBack = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush, back: mockBack });
    (useAuth as jest.Mock).mockReturnValue({ login: mockLogin, loading: false });
  });

  it('renders email and password fields', async () => {
    render(<LoginPage />);
    expect(await screen.findByLabelText(/email address/i)).toBeInTheDocument();
    expect(await screen.findByLabelText(/password/i, { selector: 'input' })).toBeInTheDocument();
  });

  it('updates input values', async () => {
    render(<LoginPage />);
    const emailInput = await screen.findByLabelText(/email address/i);
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    expect((emailInput as HTMLInputElement).value).toBe('test@example.com');
  });

  it('toggles password visibility', async () => {
    render(<LoginPage />);
    const passwordInput = await screen.findByLabelText(/password/i, { selector: 'input' });
    const toggleButton = await screen.findByRole('button', { name: /show password/i });

    expect(passwordInput).toHaveAttribute('type', 'password');
    fireEvent.click(toggleButton);
    expect(passwordInput).toHaveAttribute('type', 'text');
  });

  it('calls login on form submit', async () => {
    render(<LoginPage />);
    const emailInput = await screen.findByLabelText(/email address/i);
    const passwordInput = await screen.findByLabelText(/password/i, { selector: 'input' });

    fireEvent.change(emailInput, { target: { value: 'user@test.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    // Use stricter regex to only match the form submit button
    fireEvent.click(screen.getByRole('button', { name: /^sign in$/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('user@test.com', 'password123');
    });
  });

  it('shows error message if login fails', async () => {
    (useAuth as jest.Mock).mockReturnValue({
      login: jest.fn().mockRejectedValue(new Error('Invalid credentials')),
      loading: false,
    });

    render(<LoginPage />);
    const emailInput = await screen.findByLabelText(/email address/i);
    const passwordInput = await screen.findByLabelText(/password/i, { selector: 'input' });

    fireEvent.change(emailInput, { target: { value: 'wrong@test.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpass' } });

    // Again: stricter match avoids "Sign in with Facebook/Google"
    fireEvent.click(screen.getByRole('button', { name: /^sign in$/i }));

    expect(await screen.findByText(/invalid credentials/i)).toBeInTheDocument();
  });
});
