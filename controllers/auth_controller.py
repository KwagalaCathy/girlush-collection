"""
Authentication Controller for Girlush Collections
Handles user authentication and authorization
"""
import hashlib
from typing import Optional, Tuple
from database.database_manager import DatabaseManager
from database.models import User, Customer

class AuthController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, email: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Authenticate user
        Returns: (success, user, message)
        """
        if not email or not password:
            return False, None, "Email and password are required"

        user = self.db.get_user_by_email(email)
        if not user:
            return False, None, "Invalid email or password"

        hashed_password = self.hash_password(password)
        if user.password != hashed_password:
            return False, None, "Invalid email or password"

        return True, user, "Login successful"

    def register(self, email: str, password: str, name: str, 
                phone: str = "", address: str = "", city: str = "") -> Tuple[bool, str]:
        """
        Register new customer
        Returns: (success, message)
        """
        # Validate input
        if not email or not password or not name:
            return False, "Email, password, and name are required"

        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        # Check if email already exists
        existing_user = self.db.get_user_by_email(email)
        if existing_user:
            return False, "Email already registered"

        # Create user
        hashed_password = self.hash_password(password)
        user = User(
            email=email,
            password=hashed_password,
            name=name,
            role='customer'
        )

        user_id = self.db.create_user(user)
        if not user_id:
            return False, "Failed to create user account"

        # Create customer profile
        customer = Customer(
            user_id=user_id,
            phone=phone,
            address=address,
            city=city
        )

        customer_id = self.db.create_customer(customer)
        if not customer_id:
            return False, "Failed to create customer profile"

        return True, "Registration successful"

    def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        user = self.db.get_user_by_id(user_id)
        if not user:
            return False, "User not found"

        # Verify old password
        hashed_old = self.hash_password(old_password)
        if user.password != hashed_old:
            return False, "Current password is incorrect"

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters"

        # Update password
        user.password = self.hash_password(new_password)
        if self.db.update_user(user):
            return True, "Password changed successfully"
        else:
            return False, "Failed to change password"

    def is_admin(self, user: User) -> bool:
        """Check if user is admin"""
        return user.role == 'admin'

    def is_staff(self, user: User) -> bool:
        """Check if user is staff or admin"""
        return user.role in ['admin', 'staff']

    def is_customer(self, user: User) -> bool:
        """Check if user is customer"""
        return user.role == 'customer'
