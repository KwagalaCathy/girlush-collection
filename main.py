"""
Girlush Collections - Inventory Management System
Main Application Entry Point
"""
import tkinter as tk
from tkinter import messagebox
import os
import config
from database.database_manager import DatabaseManager
from controllers.auth_controller import AuthController
from controllers.product_controller import ProductController
from controllers.customer_controller import CustomerController
from controllers.order_controller import OrderController
from controllers.cart_controller import CartController
from views.login_view import LoginView
from views.signup_view import SignupView
from views.admin_dashboard_view import AdminDashboardView
from views.customer_dashboard_view import CustomerDashboardView

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(config.WINDOW_TITLE)
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.minsize(config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT)
        
        # Center window
        self.center_window()
        
        # Initialize database and controllers
        self.init_controllers()
        
        # Current user
        self.current_user = None
        self.current_view = None
        
        # Show login view
        self.show_login()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def init_controllers(self):
        """Initialize database and controllers"""
        # Create logs directory
        os.makedirs(config.LOG_DIR, exist_ok=True)
        
        # Initialize database
        self.db_manager = DatabaseManager()
        
        # Initialize controllers
        self.controllers = {
            'db': self.db_manager,
            'auth': AuthController(self.db_manager),
            'product': ProductController(self.db_manager),
            'customer': CustomerController(self.db_manager),
            'order': OrderController(self.db_manager),
            'cart': CartController(self.db_manager)
        }
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Show login view"""
        self.clear_window()
        self.current_view = LoginView(
            self,
            on_login_success=self.handle_login,
            on_show_signup=self.show_signup
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)
    
    def show_signup(self):
        """Show signup view"""
        self.clear_window()
        self.current_view = SignupView(
            self,
            on_signup_success=self.handle_signup,
            on_show_login=self.show_login
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)
    
    def handle_login(self, email, password):
        """Handle login attempt"""
        success, user, message = self.controllers['auth'].login(email, password)
        
        if success:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", message)
    
    def handle_signup(self, email, password, name, phone, address, city):
        """Handle signup attempt"""
        success, message = self.controllers['auth'].register(
            email, password, name, phone, address, city
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.show_login()
        else:
            messagebox.showerror("Signup Failed", message)
    
    def show_dashboard(self):
        """Show appropriate dashboard based on user role"""
        self.clear_window()
        
        if self.controllers['auth'].is_admin(self.current_user) or \
           self.controllers['auth'].is_staff(self.current_user):
            self.current_view = AdminDashboardView(
                self,
                self.current_user,
                self.controllers,
                on_logout=self.handle_logout
            )
        else:
            self.current_view = CustomerDashboardView(
                self,
                self.current_user,
                self.controllers,
                on_logout=self.handle_logout
            )
        
        self.current_view.pack(fill=tk.BOTH, expand=True)
    
    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login()

def main():
    """Main entry point"""
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
