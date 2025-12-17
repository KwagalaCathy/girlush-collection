"""
Login View for Girlush Collections
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success

class LoginView(tk.Frame):
    def __init__(self, parent, on_login_success, on_show_signup):
        super().__init__(parent, bg=config.BG_COLOR)
        self.on_login_success = on_login_success
        self.on_show_signup = on_show_signup
        
        self.create_widgets()
    
    def create_widgets(self):
        # Center container
        container = tk.Frame(self, bg=config.BG_COLOR)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo/Title
        title_label = tk.Label(
            container, 
            text=config.APP_NAME,
            font=(config.FONT_FAMILY, 32, 'bold'),
            fg=config.PRIMARY_COLOR,
            bg=config.BG_COLOR
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            container,
            text="Inventory Management System",
            font=(config.FONT_FAMILY, config.FONT_SIZE_MEDIUM),
            fg=config.TEXT_COLOR,
            bg=config.BG_COLOR
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login form
        form_frame = tk.Frame(container, bg='white', relief='solid', borderwidth=1)
        form_frame.pack(padx=40, pady=20)
        
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(padx=40, pady=40)
        
        # Email
        email_label = tk.Label(inner_frame, text="Email:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white')
        email_label.pack(anchor='w', pady=(0, 5))
        
        self.email_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=30)
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        self.email_entry.focus()
        
        # Password
        password_label = tk.Label(inner_frame, text="Password:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white')
        password_label.pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), show='*', width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Login button
        self.login_btn = tk.Button(
            inner_frame,
            text="Login",
            command=self.on_login,
            **BUTTON_STYLE,
            width=20
        )
        self.login_btn.pack(pady=(0, 10))
        
        # Signup link
        signup_frame = tk.Frame(inner_frame, bg='white')
        signup_frame.pack()
        
        tk.Label(
            signup_frame,
            text="Don't have an account?",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg='white'
        ).pack(side=tk.LEFT)
        
        signup_btn = tk.Button(
            signup_frame,
            text="Sign Up",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL, 'underline'),
            fg=config.PRIMARY_COLOR,
            bg='white',
            relief='flat',
            cursor='hand2',
            command=self.on_show_signup
        )
        signup_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.email_entry.bind('<Return>', lambda e: self.on_login())
        self.password_entry.bind('<Return>', lambda e: self.on_login())
    
    def on_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            show_error("Please enter email and password")
            return
        
        self.on_login_success(email, password)
    
    def clear_form(self):
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.focus()
