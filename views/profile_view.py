"""
Profile View for Girlush Collections - Customer
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success

class ProfileView(tk.Frame):
    def __init__(self, parent, user, controllers):
        super().__init__(parent, bg=config.BG_COLOR)
        self.user = user
        self.controllers = controllers
        
        self.create_widgets()
        self.load_profile()
    
    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text="My Profile",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
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
        
        # Bind canvas resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Cleanup
        def on_destroy(event):
            canvas.unbind_all("<MouseWheel>")
        self.bind('<Destroy>', on_destroy)
        
        # Profile form
        form_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', borderwidth=1)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(padx=40, pady=40)
        
        # Name (read-only)
        tk.Label(inner_frame, text="Name:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.name_label = tk.Label(
            inner_frame,
            text=self.user.name,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
            bg='white',
            fg=config.TEXT_COLOR
        )
        self.name_label.pack(anchor='w', pady=(0, 15))
        
        # Email (read-only)
        tk.Label(inner_frame, text="Email:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.email_label = tk.Label(
            inner_frame,
            text=self.user.email,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
            bg='white',
            fg=config.TEXT_COLOR
        )
        self.email_label.pack(anchor='w', pady=(0, 15))
        
        # Phone
        tk.Label(inner_frame, text="Phone:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.phone_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=40)
        self.phone_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Address
        tk.Label(inner_frame, text="Address:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.address_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=40)
        self.address_entry.pack(fill=tk.X, pady=(0, 15))
        
        # City
        tk.Label(inner_frame, text="City:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), bg='white').pack(anchor='w', pady=(0, 5))
        self.city_entry = tk.Entry(inner_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), width=40)
        self.city_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Update button
        tk.Button(
            inner_frame,
            text="Update Profile",
            command=self.update_profile,
            **BUTTON_STYLE
        ).pack()
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_profile(self):
        customer = self.controllers['customer'].get_customer_by_user_id(self.user.user_id)
        
        if customer:
            self.customer_id = customer.customer_id
            self.phone_entry.insert(0, customer.phone or '')
            self.address_entry.insert(0, customer.address or '')
            self.city_entry.insert(0, customer.city or '')
        else:
            self.customer_id = None
    
    def update_profile(self):
        if not self.customer_id:
            show_error("Customer profile not found")
            return
        
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        city = self.city_entry.get().strip()
        
        success, message = self.controllers['customer'].update_customer_profile(
            self.customer_id,
            phone,
            address,
            city
        )
        
        if success:
            show_success(message)
        else:
            show_error(message)
