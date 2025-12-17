"""
Order Controller for Girlush Collections
Handles order management operations
"""
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from database.database_manager import DatabaseManager
from database.models import Order, OrderItem

class OrderController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_order(self, user_id: int, customer_id: Optional[int], 
                    cart_items: List[Dict[str, Any]], payment_method: str,
                    shipping_address: str = "") -> Tuple[bool, str, Optional[int]]:
        """
        Create order from cart items
        Returns: (success, message, order_id)
        """
        if not cart_items:
            return False, "Cart is empty", None

        # Calculate total
        total_amount = 0
        order_items = []

        for item in cart_items:
            product = self.db.get_product_by_id(item['product_id'])
            if not product:
                return False, f"Product not found: {item['product_id']}", None

            if product.stock_quantity < item['quantity']:
                return False, f"Insufficient stock for {product.name}", None

            subtotal = product.price * item['quantity']
            total_amount += subtotal

            order_items.append(OrderItem(
                product_id=product.product_id,
                quantity=item['quantity'],
                unit_price=product.price,
                subtotal=subtotal
            ))

        # Create order
        order = Order(
            customer_id=customer_id,
            user_id=user_id,
            total_amount=total_amount,
            status='pending',
            payment_method=payment_method,
            shipping_address=shipping_address
        )

        order_id = self.db.create_order(order, order_items)
        if order_id:
            # Clear cart
            self.db.clear_cart(user_id)
            return True, "Order created successfully", order_id
        else:
            return False, "Failed to create order", None

    def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get order details"""
        return self.db.get_order_by_id(order_id)

    def get_all_orders(self) -> List[Dict[str, Any]]:
        """Get all orders"""
        return self.db.get_all_orders()

    def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """Get orders for a specific user"""
        return self.db.get_orders_by_user(user_id)

    def update_order_status(self, order_id: int, status: str) -> Tuple[bool, str]:
        """Update order status"""
        valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
        if status not in valid_statuses:
            return False, "Invalid status"

        if self.db.update_order_status(order_id, status):
            return True, f"Order status updated to {status}"
        else:
            return False, "Failed to update order status"

    def get_pending_orders(self) -> List[Dict[str, Any]]:
        """Get all pending orders"""
        all_orders = self.db.get_all_orders()
        return [o for o in all_orders if o['status'] == 'pending']

    def get_completed_orders(self) -> List[Dict[str, Any]]:
        """Get all completed orders"""
        all_orders = self.db.get_all_orders()
        return [o for o in all_orders if o['status'] == 'completed']
