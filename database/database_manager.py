"""
Database Manager for Girlush Collections Inventory Management System
Handles all database operations and CRUD functionality
"""
import sqlite3
import hashlib
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
import config
from database.models import User, Product, Customer, Order, OrderItem, Supplier, CartItem

class DatabaseManager:
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Create and return a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')

        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price REAL NOT NULL,
                cost REAL,
                stock_quantity INTEGER NOT NULL,
                supplier_id INTEGER,
                image_path TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
            )
        ''')

        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                phone TEXT,
                address TEXT,
                city TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                user_id INTEGER,
                order_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                payment_method TEXT,
                shipping_address TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Order Items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')

        # Suppliers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                created_at TEXT NOT NULL
            )
        ''')

        # Cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                added_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')

        # Sales table (for reporting)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                sale_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                profit REAL,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        ''')

        # Inventory Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                transaction_date TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')

        conn.commit()

        # Create default admin user if not exists
        self._create_default_admin(cursor)
        conn.commit()
        conn.close()

    def _create_default_admin(self, cursor):
        """Create default admin user"""
        hashed_password = hashlib.sha256(config.DEFAULT_ADMIN_PASSWORD.encode()).hexdigest()
        try:
            cursor.execute('''
                INSERT INTO users (email, password, name, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (config.DEFAULT_ADMIN_EMAIL, hashed_password, config.DEFAULT_ADMIN_NAME, 
                  'admin', datetime.now().isoformat()))
        except sqlite3.IntegrityError:
            pass  # Admin already exists

    # ===== USER OPERATIONS =====
    def create_user(self, user: User) -> Optional[int]:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (email, password, name, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user.email, user.password, user.name, user.role, user.created_at))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row['user_id'], row['email'], row['password'], 
                       row['name'], row['role'], row['created_at'])
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row['user_id'], row['email'], row['password'], 
                       row['name'], row['role'], row['created_at'])
        return None

    def get_all_users(self) -> List[User]:
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [User(row['user_id'], row['email'], row['password'], 
                    row['name'], row['role'], row['created_at']) for row in rows]

    def update_user(self, user: User) -> bool:
        """Update user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE users SET email = ?, name = ?, role = ?
                WHERE user_id = ?
            ''', (user.email, user.name, user.role, user.user_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    # ===== PRODUCT OPERATIONS =====
    def create_product(self, product: Product) -> Optional[int]:
        """Create a new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (name, description, category, price, cost, 
                                     stock_quantity, supplier_id, image_path, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product.name, product.description, product.category, product.price,
                  product.cost, product.stock_quantity, product.supplier_id,
                  product.image_path, product.created_at))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating product: {e}")
            return None
        finally:
            conn.close()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Product(row['product_id'], row['name'], row['description'],
                          row['category'], row['price'], row['cost'],
                          row['stock_quantity'], row['supplier_id'],
                          row['image_path'], row['created_at'])
        return None

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [Product(row['product_id'], row['name'], row['description'],
                       row['category'], row['price'], row['cost'],
                       row['stock_quantity'], row['supplier_id'],
                       row['image_path'], row['created_at']) for row in rows]

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE category = ? ORDER BY name', (category,))
        rows = cursor.fetchall()
        conn.close()
        return [Product(row['product_id'], row['name'], row['description'],
                       row['category'], row['price'], row['cost'],
                       row['stock_quantity'], row['supplier_id'],
                       row['image_path'], row['created_at']) for row in rows]

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_term = f'%{query}%'
        cursor.execute('''
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY name
        ''', (search_term, search_term, search_term))
        rows = cursor.fetchall()
        conn.close()
        return [Product(row['product_id'], row['name'], row['description'],
                       row['category'], row['price'], row['cost'],
                       row['stock_quantity'], row['supplier_id'],
                       row['image_path'], row['created_at']) for row in rows]

    def update_product(self, product: Product) -> bool:
        """Update product information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE products 
                SET name = ?, description = ?, category = ?, price = ?, cost = ?,
                    stock_quantity = ?, supplier_id = ?, image_path = ?
                WHERE product_id = ?
            ''', (product.name, product.description, product.category, product.price,
                  product.cost, product.stock_quantity, product.supplier_id,
                  product.image_path, product.product_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
        finally:
            conn.close()

    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update product stock quantity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE products 
                SET stock_quantity = stock_quantity + ?
                WHERE product_id = ?
            ''', (quantity_change, product_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    # ===== CUSTOMER OPERATIONS =====
    def create_customer(self, customer: Customer) -> Optional[int]:
        """Create a new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO customers (user_id, phone, address, city, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer.user_id, customer.phone, customer.address, 
                  customer.city, customer.created_at))
            conn.commit()
            return cursor.lastrowid
        except:
            return None
        finally:
            conn.close()

    def get_customer_by_user_id(self, user_id: int) -> Optional[Customer]:
        """Get customer by user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Customer(row['customer_id'], row['user_id'], row['phone'],
                          row['address'], row['city'], row['created_at'])
        return None

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers with user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.name, u.email 
            FROM customers c
            JOIN users u ON c.user_id = u.user_id
            ORDER BY c.created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_customer(self, customer: Customer) -> bool:
        """Update customer information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE customers 
                SET phone = ?, address = ?, city = ?
                WHERE customer_id = ?
            ''', (customer.phone, customer.address, customer.city, customer.customer_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    # ===== ORDER OPERATIONS =====
    def create_order(self, order: Order, order_items: List[OrderItem]) -> Optional[int]:
        """Create a new order with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Insert order
            cursor.execute('''
                INSERT INTO orders (customer_id, user_id, order_date, total_amount, 
                                   status, payment_method, shipping_address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (order.customer_id, order.user_id, order.order_date, order.total_amount,
                  order.status, order.payment_method, order.shipping_address))
            order_id = cursor.lastrowid

            # Insert order items
            for item in order_items:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, item.product_id, item.quantity, item.unit_price, item.subtotal))

                # Update stock
                cursor.execute('''
                    UPDATE products 
                    SET stock_quantity = stock_quantity - ?
                    WHERE product_id = ?
                ''', (item.quantity, item.product_id))

            conn.commit()
            return order_id
        except Exception as e:
            print(f"Error creating order: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get order by ID with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get order
        cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        order_row = cursor.fetchone()
        
        if not order_row:
            conn.close()
            return None

        # Get order items
        cursor.execute('''
            SELECT oi.*, p.name as product_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items_rows = cursor.fetchall()
        
        conn.close()

        order_dict = dict(order_row)
        order_dict['items'] = [dict(row) for row in items_rows]
        return order_dict

    def get_all_orders(self) -> List[Dict[str, Any]]:
        """Get all orders"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, u.name as customer_name
            FROM orders o
            LEFT JOIN users u ON o.user_id = u.user_id
            ORDER BY o.order_date DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_orders_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get orders by user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM orders 
            WHERE user_id = ?
            ORDER BY order_date DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_order_status(self, order_id: int, status: str) -> bool:
        """Update order status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE orders SET status = ? WHERE order_id = ?', 
                          (status, order_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    # ===== CART OPERATIONS =====
    def add_to_cart(self, cart_item: CartItem) -> bool:
        """Add item to cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Check if item already in cart
            cursor.execute('''
                SELECT cart_id, quantity FROM cart 
                WHERE user_id = ? AND product_id = ?
            ''', (cart_item.user_id, cart_item.product_id))
            existing = cursor.fetchone()

            if existing:
                # Update quantity
                new_quantity = existing['quantity'] + cart_item.quantity
                cursor.execute('''
                    UPDATE cart SET quantity = ? 
                    WHERE cart_id = ?
                ''', (new_quantity, existing['cart_id']))
            else:
                # Insert new item
                cursor.execute('''
                    INSERT INTO cart (user_id, product_id, quantity, added_at)
                    VALUES (?, ?, ?, ?)
                ''', (cart_item.user_id, cart_item.product_id, 
                      cart_item.quantity, cart_item.added_at))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False
        finally:
            conn.close()

    def get_cart_items(self, user_id: int) -> List[Dict[str, Any]]:
        """Get cart items for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, p.name, p.price, p.stock_quantity, p.image_path
            FROM cart c
            JOIN products p ON c.product_id = p.product_id
            WHERE c.user_id = ?
            ORDER BY c.added_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def update_cart_item_quantity(self, cart_id: int, quantity: int) -> bool:
        """Update cart item quantity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE cart SET quantity = ? WHERE cart_id = ?', 
                          (quantity, cart_id))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def remove_from_cart(self, cart_id: int) -> bool:
        """Remove item from cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM cart WHERE cart_id = ?', (cart_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def clear_cart(self, user_id: int) -> bool:
        """Clear all items from user's cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    # ===== SUPPLIER OPERATIONS =====
    def create_supplier(self, supplier: Supplier) -> Optional[int]:
        """Create a new supplier"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO suppliers (name, contact_person, email, phone, address, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (supplier.name, supplier.contact_person, supplier.email,
                  supplier.phone, supplier.address, supplier.created_at))
            conn.commit()
            return cursor.lastrowid
        except:
            return None
        finally:
            conn.close()

    def get_all_suppliers(self) -> List[Supplier]:
        """Get all suppliers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM suppliers ORDER BY name')
        rows = cursor.fetchall()
        conn.close()
        return [Supplier(row['supplier_id'], row['name'], row['contact_person'],
                        row['email'], row['phone'], row['address'], row['created_at']) 
                for row in rows]

    # ===== STATISTICS =====
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        stats = {}

        # Total products
        cursor.execute('SELECT COUNT(*) as count FROM products')
        stats['total_products'] = cursor.fetchone()['count']

        # Total customers
        cursor.execute('SELECT COUNT(*) as count FROM customers')
        stats['total_customers'] = cursor.fetchone()['count']

        # Total orders
        cursor.execute('SELECT COUNT(*) as count FROM orders')
        stats['total_orders'] = cursor.fetchone()['count']

        # Total sales
        cursor.execute('SELECT SUM(total_amount) as total FROM orders WHERE status = "completed"')
        result = cursor.fetchone()
        stats['total_sales'] = result['total'] if result['total'] else 0

        # Low stock products
        cursor.execute(f'SELECT COUNT(*) as count FROM products WHERE stock_quantity < {config.LOW_STOCK_THRESHOLD}')
        stats['low_stock_products'] = cursor.fetchone()['count']

        # Recent orders
        cursor.execute('SELECT COUNT(*) as count FROM orders WHERE status = "pending"')
        stats['pending_orders'] = cursor.fetchone()['count']

        conn.close()
        return stats

    def get_sales_data(self, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """Get sales data for reports"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT 
                DATE(order_date) as date,
                COUNT(*) as order_count,
                SUM(total_amount) as total_sales
            FROM orders
            WHERE status = "completed"
        '''
        
        params = []
        if start_date:
            query += ' AND DATE(order_date) >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND DATE(order_date) <= ?'
            params.append(end_date)
            
        query += ' GROUP BY DATE(order_date) ORDER BY date DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
