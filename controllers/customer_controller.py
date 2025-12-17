"""
Customer Controller for Girlush Collections
Handles customer management operations
"""
from typing import List, Optional, Tuple, Dict, Any
from database.database_manager import DatabaseManager
from database.models import Customer

class CustomerController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_customer_by_user_id(self, user_id: int) -> Optional[Customer]:
        """Get customer profile by user ID"""
        return self.db.get_customer_by_user_id(user_id)

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers with user information"""
        return self.db.get_all_customers()

    def update_customer_profile(self, customer_id: int, phone: str, 
                                address: str, city: str) -> Tuple[bool, str]:
        """Update customer profile"""
        customer = Customer(
            customer_id=customer_id,
            phone=phone,
            address=address,
            city=city
        )

        if self.db.update_customer(customer):
            return True, "Profile updated successfully"
        else:
            return False, "Failed to update profile"

    def search_customers(self, query: str) -> List[Dict[str, Any]]:
        """Search customers by name, email, or phone"""
        all_customers = self.db.get_all_customers()
        query_lower = query.lower()
        
        results = []
        for customer in all_customers:
            if (query_lower in customer.get('name', '').lower() or
                query_lower in customer.get('email', '').lower() or
                query_lower in customer.get('phone', '').lower()):
                results.append(customer)
        
        return results
