"""
Database models for Girlush Collections Inventory Management System
"""
from datetime import datetime
from typing import Optional, Dict, Any

class User:
    def __init__(self, user_id: Optional[int] = None, email: str = "", password: str = "", 
                 name: str = "", role: str = "customer", created_at: Optional[str] = None):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.name = name
        self.role = role  # admin, staff, customer
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at
        }

class Product:
    def __init__(self, product_id: Optional[int] = None, name: str = "", description: str = "",
                 category: str = "", price: float = 0.0, cost: float = 0.0, stock_quantity: int = 0,
                 supplier_id: Optional[int] = None, image_path: str = "", created_at: Optional[str] = None):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.cost = cost
        self.stock_quantity = stock_quantity
        self.supplier_id = supplier_id
        self.image_path = image_path
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'cost': self.cost,
            'stock_quantity': self.stock_quantity,
            'supplier_id': self.supplier_id,
            'image_path': self.image_path,
            'created_at': self.created_at
        }

class Customer:
    def __init__(self, customer_id: Optional[int] = None, user_id: Optional[int] = None,
                 phone: str = "", address: str = "", city: str = "", created_at: Optional[str] = None):
        self.customer_id = customer_id
        self.user_id = user_id
        self.phone = phone
        self.address = address
        self.city = city
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'customer_id': self.customer_id,
            'user_id': self.user_id,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'created_at': self.created_at
        }

class Order:
    def __init__(self, order_id: Optional[int] = None, customer_id: int = 0, user_id: Optional[int] = None,
                 order_date: Optional[str] = None, total_amount: float = 0.0, status: str = "pending",
                 payment_method: str = "cash", shipping_address: str = ""):
        self.order_id = order_id
        self.customer_id = customer_id
        self.user_id = user_id
        self.order_date = order_date or datetime.now().isoformat()
        self.total_amount = total_amount
        self.status = status  # pending, processing, completed, cancelled
        self.payment_method = payment_method
        self.shipping_address = shipping_address

    def to_dict(self) -> Dict[str, Any]:
        return {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'user_id': self.user_id,
            'order_date': self.order_date,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address
        }

class OrderItem:
    def __init__(self, item_id: Optional[int] = None, order_id: int = 0, product_id: int = 0,
                 quantity: int = 0, unit_price: float = 0.0, subtotal: float = 0.0):
        self.item_id = item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal

    def to_dict(self) -> Dict[str, Any]:
        return {
            'item_id': self.item_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }

class Supplier:
    def __init__(self, supplier_id: Optional[int] = None, name: str = "", contact_person: str = "",
                 email: str = "", phone: str = "", address: str = "", created_at: Optional[str] = None):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_person = contact_person
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'supplier_id': self.supplier_id,
            'name': self.name,
            'contact_person': self.contact_person,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at
        }

class CartItem:
    def __init__(self, cart_id: Optional[int] = None, user_id: int = 0, product_id: int = 0,
                 quantity: int = 0, added_at: Optional[str] = None):
        self.cart_id = cart_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.added_at = added_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'cart_id': self.cart_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'added_at': self.added_at
        }
