import { Test, TestingModule } from '@nestjs/testing';
import { WishlistService } from './wishlist.service';
import { getModelToken } from '@nestjs/mongoose';
import { Model, Types } from 'mongoose';
import { User, UserDocument } from '../auth/schemas/user.schema';
import { NotFoundException } from '@nestjs/common';

// Define a valid ObjectId string for testing purposes.
const validObjectIdString = '60c72b2f9b1d8e0a1b0d2d3c';

// Mock user object for the tests.
const mockUser = {
  _id: 'mockUserId',
  wishlist: [],
  save: jest.fn().mockResolvedValue(true),
};

// Mock user model with chained methods like findById, populate, and exec.
const mockUserModel = {
  findById: jest.fn().mockImplementation((id) => ({
    populate: jest.fn().mockReturnValue({
      exec: jest.fn().mockResolvedValue(mockUser),
    }),
  })),
};

describe('WishlistService', () => {
  let service: WishlistService;
  let userModel: Model<UserDocument>;

  beforeEach(async () => {
    // Reset mock before each test to ensure isolation.
    jest.clearAllMocks();

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        WishlistService,
        {
          provide: getModelToken(User.name),
          useValue: mockUserModel,
        },
      ],
    }).compile();

    service = module.get<WishlistService>(WishlistService);
    userModel = module.get<Model<UserDocument>>(getModelToken(User.name));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('getWishlist', () => {
    it('should return the wishlist of a user', async () => {
      const mockPopulatedWishlist = [{ _id: validObjectIdString, name: 'Product 1' }];
      (mockUserModel.findById as jest.Mock).mockReturnValue({
        populate: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue({
            ...mockUser,
            wishlist: mockPopulatedWishlist,
          }),
        }),
      });

      const wishlist = await service.getWishlist('mockUserId');
      expect(wishlist).toEqual(mockPopulatedWishlist);
      expect(userModel.findById).toHaveBeenCalledWith('mockUserId');
    });

    it('should throw NotFoundException if user is not found', async () => {
      (mockUserModel.findById as jest.Mock).mockReturnValue({
        populate: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue(null),
        }),
      });

      await expect(service.getWishlist('nonExistentUserId')).rejects.toThrow(NotFoundException);
    });
  });

  describe('toggleWishlist', () => {
    it('should add a product to the wishlist if it does not exist', async () => {
      const mockUserWithEmptyWishlist = {
        ...mockUser,
        wishlist: [],
        save: jest.fn().mockResolvedValue(true),
      };
      
      // Mock findById to return the mock user with an empty wishlist.
      (mockUserModel.findById as jest.Mock).mockResolvedValueOnce(mockUserWithEmptyWishlist);

      // Mock the second findById call (after saving) to return a populated user.
      (mockUserModel.findById as jest.Mock).mockReturnValueOnce({
        populate: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue({
            ...mockUser,
            wishlist: [new Types.ObjectId(validObjectIdString)], // The newly added product
          }),
        }),
      });

      const updatedWishlist = await service.toggleWishlist('mockUserId', validObjectIdString);
      expect(mockUserWithEmptyWishlist.wishlist.length).toBe(1);
      expect(mockUserWithEmptyWishlist.wishlist[0].equals(new Types.ObjectId(validObjectIdString))).toBe(true);
      expect(mockUserWithEmptyWishlist.save).toHaveBeenCalled();
      expect(updatedWishlist.length).toBe(1);
    });

    it('should remove a product from the wishlist if it already exists', async () => {
      const mockUserWithProduct = {
        ...mockUser,
        wishlist: [new Types.ObjectId(validObjectIdString)],
        save: jest.fn().mockResolvedValue(true),
      };
      
      // Mock findById to return the mock user with the product already in the wishlist.
      (mockUserModel.findById as jest.Mock).mockResolvedValueOnce(mockUserWithProduct);

      // Mock the second findById call (after saving) to return a user with an empty wishlist.
      (mockUserModel.findById as jest.Mock).mockReturnValueOnce({
        populate: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue({
            ...mockUser,
            wishlist: [],
          }),
        }),
      });

      const updatedWishlist = await service.toggleWishlist('mockUserId', validObjectIdString);
      expect(mockUserWithProduct.wishlist.length).toBe(0);
      expect(mockUserWithProduct.save).toHaveBeenCalled();
      expect(updatedWishlist.length).toBe(0);
    });

    it('should throw NotFoundException if user is not found during toggle', async () => {
      (mockUserModel.findById as jest.Mock).mockResolvedValueOnce(null);

      await expect(service.toggleWishlist('nonExistentUserId', validObjectIdString)).rejects.toThrow(NotFoundException);
    });
  });
});
