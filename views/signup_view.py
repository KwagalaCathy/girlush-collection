"""
Signup View for Girlush Collections
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success

class SignupView(tk.Frame):
    def __init__(self, parent, on_signup_success, on_show_login):
        super().__init__(parent, bg=config.BG_COLOR)
        self.on_signup_success = on_signup_success
        self.on_show_login = on_show_login
        
        self.create_widgets()
    
    def create_widgets(self):
        # Scrollable container
        canvas = tk.Canvas(self, bg=config.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind canvas resize to update window width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Unbind mousewheel when widget is destroyed
        def on_destroy(event):
            canvas.unbind_all("<MouseWheel>")
        self.bind('<Destroy>', on_destroy)
        
        # Center container with proper alignment
        container_wrapper = tk.Frame(scrollable_frame, bg=config.BG_COLOR)
        container_wrapper.pack(fill=tk.BOTH, expand=True)
        
        container = tk.Frame(container_wrapper, bg=config.BG_COLOR)
        container.pack(expand=True, pady=50)
        
        # Center horizontally
        for widget in [container]:
            widget.pack_configure(anchor=tk.CENTER)
        
        # Create centered inner frame
        center_frame = tk.Frame(container, bg=config.BG_COLOR)
        center_frame.pack(anchor=tk.CENTER)
        
        # Title
        title_label = tk.Label(
            center_frame,
            text="Create Account",
            font=(config.FONT_FAMILY, 24, 'bold'),
            fg=config.PRIMARY_COLOR,
            bg=config.BG_COLOR
        )
        title_label.pack(pady=(0, 30))
        
        # Signup form
        form_frame = tk.Frame(center_frame, bg='white', relief='solid', borderwidth=1)
        form_frame.pack(padx=40, pady=20)
        
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(padx=40, pady=40)
        
        # Name
        tk.Label(inner_frame, text="Full Name:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.name_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=30)
        self.name_entry.pack(fill=tk.X, pady=(0, 15))
        self.name_entry.focus()
        
        # Email
        tk.Label(inner_frame, text="Email:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.email_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=30)
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        tk.Label(inner_frame, text="Password:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.password_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), show='*', width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm Password
        tk.Label(inner_frame, text="Confirm Password:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.confirm_password_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), show='*', width=30)
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Phone
        tk.Label(inner_frame, text="Phone (optional):", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.phone_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=30)
        self.phone_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Address
        tk.Label(inner_frame, text="Address (optional):", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.address_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=30)
        self.address_entry.pack(fill=tk.X, pady=(0, 15))
        
        # City
        tk.Label(inner_frame, text="City (optional):", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.city_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=30)
        self.city_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Signup button
        self.signup_btn = tk.Button(
            inner_frame,
            text="Sign Up",
            command=self.on_signup,
            **BUTTON_STYLE,
            width=20
        )
        self.signup_btn.pack(pady=(0, 10))
        
        # Login link
        login_frame = tk.Frame(inner_frame, bg='white')
        login_frame.pack()
        
        tk.Label(
            login_frame,
            text="Already have an account?",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg='white'
        ).pack(side=tk.LEFT)
        
        login_btn = tk.Button(
            login_frame,
            text="Login",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL, 'underline'),
            fg=config.PRIMARY_COLOR,
            bg='white',
            relief='flat',
            cursor='hand2',
            command=self.on_show_login
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_signup(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        city = self.city_entry.get().strip()
        
        if not name or not email or not password:
            show_error("Please fill in all required fields")
            return
        
        if password != confirm_password:
            show_error("Passwords do not match")
            return
        
        self.on_signup_success(email, password, name, phone, address, city)
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.city_entry.delete(0, tk.END)
        self.name_entry.focus()
