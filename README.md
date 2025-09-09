# The Luxe 🏡✨

<div align="center">
  <img src="https://img.shields.io/badge/Next.js-14.0-black?style=for-the-badge&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/NestJS-10.0-ea2845?style=for-the-badge&logo=nestjs" alt="NestJS">
  <img src="https://img.shields.io/badge/MongoDB-6.0-47A248?style=for-the-badge&logo=mongodb" alt="MongoDB">
  <img src="https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript" alt="TypeScript">
  <img src="https://img.shields.io/badge/TailwindCSS-3.3-06B6D4?style=for-the-badge&logo=tailwindcss" alt="TailwindCSS">
</div>

<div align="center">
  <h3>A Modern Full-Stack E-Commerce Platform for Premium Home Decor</h3>
  <p>Built with Next.js, NestJS, and MongoDB • Featuring Role-Based Access Control • Cloud Image Management</p>
</div>

---

## 🌟 Overview

**The Luxe** is a sophisticated, full-stack e-commerce application designed specifically for the home decor market. It combines a powerful NestJS backend API with a sleek Next.js frontend to deliver an exceptional shopping experience for buyers and a comprehensive management platform for sellers.

### 🎯 Key Highlights
- **Modern Architecture**: Built with cutting-edge technologies for optimal performance
- **Role-Based System**: Distinct experiences for buyers and sellers
- **Cloud Integration**: Seamless image management with Cloudinary
- **Secure Authentication**: JWT-based authentication with bcrypt encryption
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-time Features**: Dynamic cart management and instant product updates

---

## 🚀 Features

### 👥 **For Buyers**
- 🔍 **Advanced Product Discovery**
  - Browse extensive home decor collections
  - Smart search functionality with filters
  - Category and niche-based filtering
  - Product recommendations

- 📱 **Seamless Shopping Experience**
  - Detailed product pages with high-quality images
  - Interactive shopping cart with quantity management
  - Personal wishlist for favorite items
  - Secure checkout process

- 💬 **Community Features**
  - Read authentic user reviews
  - Write and share product experiences
  - Rating system for informed decisions

- 🔐 **Secure Account Management**
  - Easy registration and login
  - Profile customization
  - Order history tracking
  - Token-based authentication

### 🏪 **For Sellers**
- 📦 **Complete Product Management**
  - Create, edit, and delete products
  - Bulk product operations
  - Inventory tracking
  - Product performance analytics

- 🖼️ **Rich Media Management**
  - Multi-image product uploads
  - Cloudinary-powered image optimization
  - Drag-and-drop image organization
  - Automatic image compression

- 🛡️ **Role-Based Security**
  - Protected seller routes
  - Secure API endpoints
  - Permission-based access control
  - Activity logging

- 📊 **Business Tools**
  - Sales dashboard
  - Product performance metrics
  - Customer engagement insights

---

## 🛠️ Technology Stack

### **Frontend (Next.js)**
| Technology | Purpose | Version |
|------------|---------|---------|
| [Next.js](https://nextjs.org/) | React Framework | 14.x |
| [TypeScript](https://www.typescriptlang.org/) | Type Safety | 5.x |
| [Tailwind CSS](https://tailwindcss.com/) | Styling Framework | 3.x |
| [Framer Motion](https://www.framer.com/motion/) | Animations | Latest |
| [React Hot Toast](https://react-hot-toast.com/) | Notifications | Latest |
| [Lucide React](https://lucide.dev/) | Icon Library | Latest |
| [Next Auth](https://next-auth.js.org/) | Authentication | Latest |
| [Heroicons](https://heroicons.com/) | Additional Icons | Latest |

### **Backend (NestJS)**
| Technology | Purpose | Version |
|------------|---------|---------|
| [NestJS](https://nestjs.com/) | Node.js Framework | 10.x |
| [MongoDB](https://www.mongodb.com/) | Database | 6.x |
| [Mongoose](https://mongoosejs.com/) | ODM | Latest |
| [JWT](https://jwt.io/) | Authentication | Latest |
| [bcrypt](https://www.npmjs.com/package/bcrypt) | Password Hashing | Latest |
| [Cloudinary](https://cloudinary.com/) | Image Management | Latest |
| [Passport](http://www.passportjs.org/) | Authentication Middleware | Latest |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your development machine:

- **Node.js** (version 18.0 or higher) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn** - [Yarn Installation](https://yarnpkg.com/getting-started/install)
- **MongoDB** (version 6.0 or higher) - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/)

### Optional Tools
- **MongoDB Compass** - GUI for MongoDB
- **Postman** - API testing tool
- **VS Code** - Recommended code editor

---

## ⚡ Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/the-luxe.git
cd the-luxe
```

### 2. **Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env with your configurations
# Add your MongoDB connection string and JWT secret
```

**Environment Variables (.env):**
```env
# Database
MONGODB_URI=mongodb://localhost:27017/the-luxe
DB_NAME=the-luxe

# Authentication
JWT_SECRET=your-super-secure-jwt-secret-key
JWT_EXPIRES_IN=7d

# Cloudinary (for image uploads)
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Server
PORT=3000
NODE_ENV=development
```

```bash
# Start the backend server
npm run start:dev
```

### 3. **Frontend Setup**
```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local with your configurations
```

**Environment Variables (.env.local):**
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3001

# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3001
NEXTAUTH_SECRET=your-nextauth-secret

# External Services
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your-cloudinary-name
```

```bash
# Start the frontend development server
npm run dev
```

### 4. **Access the Application**
- **Frontend**: [http://localhost:3001](http://localhost:3001)
- **Backend API**: [http://localhost:3000](http://localhost:3000)
- **API Documentation**: [http://localhost:3000/api](http://localhost:3000/api)

---

## 📚 API Documentation

### **Authentication Endpoints**
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/auth/register` | Register a new user | Public |
| `POST` | `/auth/login` | User login | Public |
| `POST` | `/auth/logout` | User logout | Authenticated |
| `GET` | `/auth/profile` | Get user profile | Authenticated |
| `PUT` | `/auth/profile` | Update user profile | Authenticated |

### **Product Endpoints**
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/products` | Get all products | Public |
| `GET` | `/products/:id` | Get product by ID | Public |
| `GET` | `/products/me` | Get seller's products | Seller |
| `POST` | `/products` | Create new product | Seller |
| `PUT` | `/products/:id` | Update product | Seller (Owner) |
| `DELETE` | `/products/:id` | Delete product | Seller (Owner) |
| `GET` | `/products/search` | Search products | Public |
| `GET` | `/products/category/:category` | Get products by category | Public |

### **Cart Endpoints**
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/cart` | Get user's cart | Buyer |
| `POST` | `/cart` | Add item to cart | Buyer |
| `PUT` | `/cart/:id` | Update cart item | Buyer |
| `DELETE` | `/cart/:id` | Remove item from cart | Buyer |
| `DELETE` | `/cart` | Clear entire cart | Buyer |

### **Wishlist Endpoints**
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/wishlist` | Get user's wishlist | Buyer |
| `POST` | `/wishlist` | Add item to wishlist | Buyer |
| `DELETE` | `/wishlist/:id` | Remove item from wishlist | Buyer |

### **Review Endpoints**
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/reviews/:productId` | Get product reviews | Public |
| `POST` | `/reviews` | Create a review | Buyer |
| `PUT` | `/reviews/:id` | Update review | Buyer (Owner) |
| `DELETE` | `/reviews/:id` | Delete review | Buyer (Owner) |

---

## 🏗️ Project Structure

```
the-luxe/
│
├── backend/                 # NestJS Backend
│   ├── src/
│   │   ├── auth/           # Authentication module
│   │   ├── products/       # Products module
│   │   ├── cart/           # Shopping cart module
│   │   ├── users/          # User management module
│   │   ├── reviews/        # Reviews module
│   │   ├── upload/         # File upload module
│   │   ├── common/         # Shared utilities
│   │   └── main.ts         # Application entry point
│   ├── test/               # Test files
│   ├── .env.example        # Environment variables template
│   ├── package.json
│   └── README.md
│
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # Reusable components
│   │   ├── context/       # React contexts
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Utility libraries
│   │   ├── types/         # TypeScript types
│   │   └── styles/        # Global styles
│   ├── public/            # Static assets
│   ├── .env.local.example # Environment variables template
│   ├── package.json
│   └── README.md
│
├── docs/                   # Documentation
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🔧 Development

### **Available Scripts**

#### Backend
```bash
# Development
npm run start:dev          # Start in development mode
npm run start:debug        # Start in debug mode
npm run start:prod         # Start in production mode

# Building
npm run build              # Build the application
npm run prebuild           # Pre-build tasks

# Testing
npm run test               # Run unit tests
npm run test:e2e           # Run end-to-end tests
npm run test:cov           # Run tests with coverage

# Code Quality
npm run lint               # Lint the code
npm run format             # Format the code
```

#### Frontend
```bash
# Development
npm run dev                # Start development server
npm run build              # Build for production
npm run start              # Start production server
npm run lint               # Lint the code

# Testing
npm run test               # Run tests
npm run test:watch         # Run tests in watch mode

# Code Quality
npm run type-check         # TypeScript type checking
npm run format             # Format the code
```

### **Environment Setup**

#### Development
1. Use `npm run start:dev` for backend hot-reloading
2. Use `npm run dev` for frontend hot-reloading
3. MongoDB should be running locally or via cloud

#### Production
1. Build both applications: `npm run build`
2. Use environment variables for production settings
3. Consider using PM2 for process management
4. Set up reverse proxy with Nginx

---

## 🧪 Testing

### **Running Tests**
```bash
# Backend tests
cd backend
npm run test              # Unit tests
npm run test:e2e         # End-to-end tests
npm run test:cov         # Coverage report

# Frontend tests
cd frontend
npm run test             # Component tests
npm run test:watch       # Watch mode
```

### **Test Coverage**
- **Backend**: Unit tests for services, controllers, and guards
- **Frontend**: Component tests, integration tests, and E2E tests
- **API**: Comprehensive endpoint testing with different user roles

---

## 🚀 Deployment

### **Prerequisites for Deployment**
- Node.js 18+ runtime environment
- MongoDB database (local or cloud)
- Cloudinary account for image management
- Domain name (optional)

### **Deployment Options**

#### **Option 1: Traditional VPS/Server**
```bash
# Clone and build
git clone <repository-url>
cd the-luxe

# Backend deployment
cd backend
npm install --production
npm run build
npm start

# Frontend deployment
cd frontend
npm install --production
npm run build
npm start
```

#### **Option 2: Container Deployment (Docker)**
```dockerfile
# Dockerfile example for backend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start:prod"]
```

#### **Option 3: Cloud Platforms**
- **Vercel** (recommended for frontend)
- **Railway** or **Render** (for backend)
- **MongoDB Atlas** (for database)
- **Cloudinary** (for image storage)

### **Environment Variables for Production**
Ensure all environment variables are properly configured in your production environment:
- Database connection strings
- JWT secrets
- API keys
- CORS settings
- Domain configurations

---

## 🤝 Contributing

We welcome contributions from the community! Please follow these guidelines:

### **Getting Started**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `npm test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### **Code Style**
- Follow the existing code style
- Use TypeScript for type safety
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

### **Pull Request Process**
1. Ensure all tests pass
2. Update the README.md if needed
3. Add screenshots for UI changes
4. Request review from maintainers
