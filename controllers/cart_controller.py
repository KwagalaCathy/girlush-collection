"""
Cart Controller for Girlush Collections
Handles shopping cart operations
"""
from typing import List, Tuple, Dict, Any
from database.database_manager import DatabaseManager
from database.models import CartItem

class CartController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> Tuple[bool, str]:
        """Add product to cart"""
        # Validate product exists and has stock
        product = self.db.get_product_by_id(product_id)
        if not product:
            return False, "Product not found"

        if product.stock_quantity < quantity:
            return False, f"Only {product.stock_quantity} items available in stock"

        if quantity <= 0:
            return False, "Quantity must be greater than 0"

        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )

        if self.db.add_to_cart(cart_item):
            return True, "Added to cart"
        else:
            return False, "Failed to add to cart"

    def get_cart_items(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all cart items for user"""
        return self.db.get_cart_items(user_id)

    def update_quantity(self, cart_id: int, quantity: int) -> Tuple[bool, str]:
        """Update cart item quantity"""
        if quantity <= 0:
            return False, "Quantity must be greater than 0"

        if self.db.update_cart_item_quantity(cart_id, quantity):
            return True, "Quantity updated"
        else:
            return False, "Failed to update quantity"
    
    def update_cart_quantity(self, cart_id: int, quantity: int) -> Tuple[bool, str]:
        """Update cart item quantity (alias for update_quantity)"""
        return self.update_quantity(cart_id, quantity)

    def remove_from_cart(self, cart_id: int) -> Tuple[bool, str]:
        """Remove item from cart"""
        if self.db.remove_from_cart(cart_id):
            return True, "Item removed from cart"
        else:
            return False, "Failed to remove item"

    def clear_cart(self, user_id: int) -> Tuple[bool, str]:
        """Clear all items from cart"""
        if self.db.clear_cart(user_id):
            return True, "Cart cleared"
        else:
            return False, "Failed to clear cart"

    def get_cart_total(self, user_id: int) -> float:
        """Calculate cart total"""
        items = self.db.get_cart_items(user_id)
        total = sum(item['price'] * item['quantity'] for item in items)
        return total

    def get_cart_count(self, user_id: int) -> int:
        """Get number of items in cart"""
        items = self.db.get_cart_items(user_id)
        return sum(item['quantity'] for item in items)
