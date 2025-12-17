"""
Product Controller for Girlush Collections
Handles product management operations
"""
from typing import List, Optional, Tuple
from database.database_manager import DatabaseManager
from database.models import Product

class ProductController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_product(self, name: str, description: str, category: str, 
                      price: float, cost: float, stock_quantity: int,
                      supplier_id: Optional[int] = None, 
                      image_path: str = "") -> Tuple[bool, str]:
        """Create a new product"""
        # Validate input
        if not name or not category:
            return False, "Name and category are required"

        if price <= 0:
            return False, "Price must be greater than 0"

        if stock_quantity < 0:
            return False, "Stock quantity cannot be negative"

        product = Product(
            name=name,
            description=description,
            category=category,
            price=price,
            cost=cost,
            stock_quantity=stock_quantity,
            supplier_id=supplier_id,
            image_path=image_path
        )

        product_id = self.db.create_product(product)
        if product_id:
            return True, "Product created successfully"
        else:
            return False, "Failed to create product"

    def update_product(self, product_id: int, name: str, description: str, 
                      category: str, price: float, cost: float, 
                      stock_quantity: int, supplier_id: Optional[int] = None,
                      image_path: str = "") -> Tuple[bool, str]:
        """Update product information"""
        # Validate input
        if not name or not category:
            return False, "Name and category are required"

        if price <= 0:
            return False, "Price must be greater than 0"

        if stock_quantity < 0:
            return False, "Stock quantity cannot be negative"

        product = Product(
            product_id=product_id,
            name=name,
            description=description,
            category=category,
            price=price,
            cost=cost,
            stock_quantity=stock_quantity,
            supplier_id=supplier_id,
            image_path=image_path
        )

        if self.db.update_product(product):
            return True, "Product updated successfully"
        else:
            return False, "Failed to update product"

    def delete_product(self, product_id: int) -> Tuple[bool, str]:
        """Delete a product"""
        if self.db.delete_product(product_id):
            return True, "Product deleted successfully"
        else:
            return False, "Failed to delete product"

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.get_product_by_id(product_id)

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.db.get_all_products()

    def search_products(self, query: str) -> List[Product]:
        """Search products"""
        return self.db.search_products(query)

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return self.db.get_products_by_category(category)

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        all_products = self.db.get_all_products()
        return [p for p in all_products if p.stock_quantity < threshold]

    def update_stock(self, product_id: int, quantity_change: int) -> Tuple[bool, str]:
        """Update product stock"""
        product = self.db.get_product_by_id(product_id)
        if not product:
            return False, "Product not found"

        new_quantity = product.stock_quantity + quantity_change
        if new_quantity < 0:
            return False, "Insufficient stock"

        if self.db.update_stock(product_id, quantity_change):
            return True, "Stock updated successfully"
        else:
            return False, "Failed to update stock"

    def get_categories(self) -> List[str]:
        """Get all unique product categories"""
        products = self.db.get_all_products()
        categories = set(p.category for p in products if p.category)
        return sorted(list(categories))
