# Girlush Collections - Inventory Management System

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A comprehensive desktop inventory management system for handbag retail business built with Python and Tkinter, following the **MVC (Model-View-Controller)** architecture pattern.

## ✨ Features

### Admin Features
- 📊 **Dashboard**: Real-time statistics and analytics
- 📦 **Product Management**: Add, edit, delete, and track products
- 👥 **Customer Management**: Manage customer information and history
- 📋 **Order Management**: Process and track orders
- 💰 **Sales Reports**: Generate and view sales analytics
- 🏢 **Supplier Management**: Track supplier information
- 👤 **User Management**: Manage staff and admin accounts
- 📈 **Inventory Tracking**: Real-time stock levels and alerts

### Customer Features
- 🛍️ **Shop**: Browse available products
- 🛒 **Shopping Cart**: Add products to cart
- 📦 **Order History**: View past orders
- ❤️ **Wishlist**: Save favorite products
- 👤 **Profile Management**: Update personal information

### General Features
- 🔐 **Secure Authentication**: Password hashing with SHA-256
- 👥 **Role-Based Access Control**: Admin, Staff, and Customer roles
- 🎨 **Modern UI**: Clean and intuitive interface
- 💾 **SQLite Database**: Lightweight and portable
- 📱 **Responsive Design**: Adapts to different screen sizes

## 🏗️ Architecture - MVC Pattern

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│                      (main.py)                          │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌─────▼─────┐      ┌─────▼─────┐
   │  MODEL  │◄───────│CONTROLLER │─────►│   VIEW    │
   └─────────┘        └───────────┘      └───────────┘
   database/          controllers/        views/
   - models.py        - auth_controller   - login_view
   - database_mgr     - product_ctrl      - dashboard_view
                      - customer_ctrl     - products_view
                      - order_ctrl        - etc.
                      - cart_ctrl
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/girlush_collections.git
cd girlush_collections

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Default Admin Login
- **Email**: xandercaitlyn0@gmail.com
- **Password**: cathie

## 🔨 Building Executable



The executable will be in `dist/GirlushCollections.exe`

### Manual Build
```bash
pip install pyinstaller
pyinstaller build_exe.spec --clean --noconfirm
```

## 📁 Project Structure (MVC)

```
girlush_collections/
│
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── build_exe.spec # Build scripts
│
├── database/ (MODEL)          # Data Layer
│   ├── __init__.py
│   ├── database_manager.py    # CRUD operations
│   └── models.py              # Data models
│
├── controllers/ (CONTROLLER)  # Business Logic Layer
│   ├── __init__.py
│   ├── auth_controller.py     # Authentication logic
│   ├── product_controller.py  # Product logic
│   ├── customer_controller.py # Customer logic
│   ├── order_controller.py    # Order logic
│   └── cart_controller.py     # Cart logic
│
├── views/ (VIEW)              # Presentation Layer
│   ├── __init__.py
│   ├── login_view.py          # Login UI
│   ├── signup_view.py         # Signup UI
│   ├── admin_dashboard_view.py
│   ├── customer_dashboard_view.py
│   ├── dashboard_view.py      # Fallback dashboard
│   ├── products_view.py       # Product management UI
│   ├── customers_view.py      # Customer management UI
│   ├── orders_view.py         # Order management UI
│   ├── cart_view.py           # Shopping cart UI
│   ├── shop_view.py           # Product browsing UI
│   ├── sales_view.py          # Sales reports UI
│   ├── reports_view.py        # Analytics UI
│   ├── admin_inventory_view.py
│   ├── admin_orders_view.py
│   └── profile_view.py        # User profile UI
│
├── assets/                    # UI Resources
│   └── styles.py
│
├── utils/                     # Utilities
│   └── helpers.py
│
├── components/                # Reusable Components
│   └── dialogs.py
│
└── logs/                      # Application logs
```

## 🗄️ Database Schema

### Key Tables
- **users**: User accounts (admin, staff, customer)
- **products**: Product inventory
- **customers**: Customer information
- **orders**: Order records
- **order_items**: Order line items
- **suppliers**: Supplier information
- **inventory_transactions**: Stock movements
- **sales**: Sales summary

## 🚀 Usage

### Admin Workflow
1. Login with admin credentials
2. View dashboard statistics
3. Manage products, customers, orders
4. Generate sales reports
5. Manage user accounts

### Customer Workflow
1. Login/Register
2. Browse products in shop
3. Add items to cart
4. Place orders
5. View order history

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Submit pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👥 Authors

Girlush Collections Team

## 📞 Support

Email: admin@girlush.com

---

Made with ❤️ by Girlush Collections Team
