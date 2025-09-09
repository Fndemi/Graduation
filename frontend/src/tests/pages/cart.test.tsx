// import { render, screen, waitFor } from '@testing-library/react';
// import userEvent from '@testing-library/user-event';
// import CartPage from '@/app/cart/page';

// import { fetchCart, removeFromCart, updateCartItem } from '@/app/lib/cart-api';
// import { toast } from 'react-hot-toast';

// // This needs to be added to mock the matchMedia API used by react-hot-toast
// Object.defineProperty(window, 'matchMedia', {
//   writable: true,
//   value: (query) => ({
//     matches: false,
//     media: query,
//     onchange: null,
//     addListener: jest.fn(), // Deprecated
//     removeListener: jest.fn(), // Deprecated
//     addEventListener: jest.fn(),
//     removeEventListener: jest.fn(),
//     dispatchEvent: jest.fn(),
//   }),
// });

// // Mock the API functions
// jest.mock('@/app/lib/cart-api', () => ({
//   fetchCart: jest.fn(),
//   removeFromCart: jest.fn(),
//   updateCartItem: jest.fn(),
// }));

// // Mock the toast library
// jest.mock('react-hot-toast', () => ({
//   __esModule: true,
//   ...jest.requireActual('react-hot-toast'),
//   toast: {
//     success: jest.fn(),
//     error: jest.fn(),
//   },
// }));

// // Mock the Next.js Image component to prevent errors
// jest.mock('next/image', () => {
//   return (props) => <img {...props} />;
// });

// const mockCartItems = [
//   {
//     _id: "60c72b2f9b1d8b001c8e4d2a",
//     productId: {
//       _id: "60c72b2f9b1d8b001c8e4d2b",
//       name: "Wireless Mouse",
//       initialPrice: 2000,
//       discountedPrice: 1800,
//       category: "Electronics",
//       niche: "Gaming",
//       image: "/images/mouse.jpg",
//     },
//     quantity: 2,
//   },
//   {
//     _id: "60c72b2f9b1d8b001c8e4d2c",
//     productId: {
//       _2_id: "60c72b2f9b1d8b001c8e4d2d",
//       name: "Mechanical Keyboard",
//       initialPrice: 5000,
//       discountedPrice: 4500,
//       category: "Electronics",
//       niche: "Gaming",
//       image: "/images/keyboard.jpg",
//     },
//     quantity: 1,
//   },
// ];

// describe('CartPage', () => {
//   // Clear mocks before each test to ensure a clean state
//   beforeEach(() => {
//     jest.clearAllMocks();
//   });

//   it('should render "Loading cart..." initially', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue(mockCartItems);
//     render(<CartPage />);
//     expect(screen.getByText(/loading cart.../i)).toBeInTheDocument();
    
//     await waitFor(() => expect(screen.queryByText(/loading cart.../i)).not.toBeInTheDocument());
//   });

//   it('should display "Your cart is empty." when there are no items', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue([]);
//     render(<CartPage />);
//     await waitFor(() => {
//       expect(screen.getByText(/Your cart is empty./i)).toBeInTheDocument();
//       expect(screen.getByText(/Browse Products/i)).toBeInTheDocument();
//     });
//   });

//   it('should render cart items and calculate total price correctly', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue(mockCartItems);
//     render(<CartPage />);
    
//     await waitFor(() => {
//       expect(screen.getByText(/Wireless Mouse/i)).toBeInTheDocument();
//       expect(screen.getByText(/Mechanical Keyboard/i)).toBeInTheDocument();

//       // Fix 1: Use a more specific query to avoid multiple matches for '/1/'
//       // Check for quantity of the first item (2)
//       expect(screen.getByText('2')).toBeInTheDocument(); 
//       // Check for quantity of the second item (1)
//       expect(screen.getByText('1')).toBeInTheDocument();
      
//       const expectedTotal = (1800 * 2) + (4500 * 1);
//       expect(screen.getByText(`Total: Ksh ${expectedTotal.toLocaleString()}`)).toBeInTheDocument();
//     });
//   });

//   it('should increase item quantity on "+" button click', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue(mockCartItems);
//     (updateCartItem as jest.Mock).mockResolvedValue([
//       { ...mockCartItems[0], quantity: 3 },
//       mockCartItems[1]
//     ]);
    
//     render(<CartPage />);
    
//     await waitFor(() => expect(screen.getByText(/Wireless Mouse/i)).toBeInTheDocument());
    
//     const increaseButton = screen.getAllByRole('button', { name: '+' })[0];
//     await userEvent.click(increaseButton);
    
//     expect(updateCartItem).toHaveBeenCalledWith(mockCartItems[0].productId._id, 3);
    
//     await waitFor(() => expect(screen.getByText(/Ksh 1,800 x 3/)).toBeInTheDocument());
    
//     expect(toast.success).toHaveBeenCalledWith("Quantity updated!");
//   });

//   it('should decrease item quantity on "-" button click', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue(mockCartItems);
//     (updateCartItem as jest.Mock).mockResolvedValue([
//       { ...mockCartItems[0], quantity: 1 },
//       mockCartItems[1]
//     ]);
    
//     render(<CartPage />);
    
//     await waitFor(() => expect(screen.getByText(/Wireless Mouse/i)).toBeInTheDocument());
    
//     const decreaseButton = screen.getAllByRole('button', { name: '-' })[0];
//     await userEvent.click(decreaseButton);
    
//     expect(updateCartItem).toHaveBeenCalledWith(mockCartItems[0].productId._id, 1);
    
//     await waitFor(() => expect(screen.getByText(/Ksh 1,800 x 1/)).toBeInTheDocument());
//     expect(toast.success).toHaveBeenCalledWith("Quantity updated!");
//   });

//   it('should remove an item from the cart on "Remove" button click', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue(mockCartItems);
//     (removeFromCart as jest.Mock).mockResolvedValue([mockCartItems[1]]);
    
//     render(<CartPage />);
    
//     await waitFor(() => expect(screen.getByText(/Wireless Mouse/i)).toBeInTheDocument());
    
//     const removeButton = screen.getAllByRole('button', { name: /remove/i })[0];
//     await userEvent.click(removeButton);
    
//     expect(removeFromCart).toHaveBeenCalledWith(mockCartItems[0].productId._id);
    
//     await waitFor(() => {
//       expect(screen.queryByText(/Wireless Mouse/i)).not.toBeInTheDocument();
//       expect(screen.getByText(/Mechanical Keyboard/i)).toBeInTheDocument();
//       expect(toast.success).toHaveBeenCalledWith("Item removed successfully!");
//     });
//   });

//   it('should open the CheckoutModal when the "Checkout" button is clicked', async () => {
//     (fetchCart as jest.Mock).mockResolvedValue(mockCartItems);
//     render(<CartPage />);
    
//     await waitFor(() => expect(screen.getByText(/Checkout/i)).toBeInTheDocument());
    
//     const checkoutButton = screen.getByRole('button', { name: /checkout/i });
//     await userEvent.click(checkoutButton);
    
//     await waitFor(() => {
//       expect(screen.getByText(/Checkout Summary/i)).toBeInTheDocument();
//     });
//   });
// });