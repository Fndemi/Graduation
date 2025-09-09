import { Test, TestingModule } from '@nestjs/testing';
import { WishlistController } from './wishlist.controller';
import { WishlistService } from './wishlist.service';
import { AuthenticationGuard } from '../guards/authentication.guard';
import { ExecutionContext } from '@nestjs/common';

// Mock the AuthenticationGuard to bypass authentication logic in the test.
const mockAuthGuard = {
  canActivate: (context: ExecutionContext) => {
    // We can define a mock user here for the request object.
    const request = context.switchToHttp().getRequest();
    request.user = { id: 'mockUserId' };
    return true; // Always return true to allow the request to proceed.
  },
};

// Mock the WishlistService to control its behavior during the test.
const mockWishlistService = {
  getWishlist: jest.fn(),
  toggleWishlist: jest.fn(),
};

describe('WishlistController', () => {
  let controller: WishlistController;
  let service: WishlistService;

  beforeEach(async () => {
    // Create a NestJS testing module.
    const module: TestingModule = await Test.createTestingModule({
      controllers: [WishlistController],
      providers: [
        // Provide the mock WishlistService instead of the real one.
        {
          provide: WishlistService,
          useValue: mockWishlistService,
        },
      ],
    })
      // Override the real AuthenticationGuard with our mock.
      .overrideGuard(AuthenticationGuard)
      .useValue(mockAuthGuard)
      .compile();

    controller = module.get<WishlistController>(WishlistController);
    service = module.get<WishlistService>(WishlistService);
  });

  // Basic check to ensure the controller is defined.
  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('getWishlist', () => {
    it('should call wishlistService.getWishlist with the user ID', () => {
      // Mock request object, the user ID is added by the mockAuthGuard.
      const mockReq = { user: { id: 'mockUserId' } };
      
      // Call the controller method with the mock request.
      controller.getWishlist(mockReq);

      // Assert that the mocked service method was called with the correct argument.
      expect(service.getWishlist).toHaveBeenCalledWith('mockUserId');
    });
  });

  describe('toggleWishlist', () => {
    it('should call wishlistService.toggleWishlist with user and product IDs', () => {
      // Define a mock product ID.
      const productId = 'mockProductId';
      // Mock request object, the user ID is added by the mockAuthGuard.
      const mockReq = { user: { id: 'mockUserId' } };

      // Call the controller method.
      controller.toggleWishlist(mockReq, productId);

      // Assert that the mocked service method was called with the correct arguments.
      expect(service.toggleWishlist).toHaveBeenCalledWith('mockUserId', productId);
    });
  });
});
