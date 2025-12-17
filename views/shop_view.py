"""
Shop View for Girlush Collections - Customer
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success
from utils.helpers import format_currency

class ShopView(tk.Frame):
    def __init__(self, parent, user, controllers, update_cart_callback):
        super().__init__(parent, bg=config.BG_COLOR)
        self.user = user
        self.controllers = controllers
        self.update_cart_callback = update_cart_callback
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Shop Products",
            **LABEL_TITLE_STYLE
        ).pack(side=tk.LEFT)
        
        # Search
        search_frame = tk.Frame(self, bg=config.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", **LABEL_STYLE).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, **ENTRY_STYLE, width=30)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        # Products grid
        canvas = tk.Canvas(self, bg=config.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=config.BG_COLOR)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
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
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_products(self):
        # Clear products
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get products
        products = self.controllers['product'].get_all_products()
        
        # Display products in grid
        row = 0
        col = 0
        max_cols = 3
        
        for product in products:
            if product.stock_quantity > 0:  # Only show in-stock products
                product_card = self.create_product_card(product)
                product_card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # Configure grid columns
        for i in range(max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
    
    def create_product_card(self, product):
        card = tk.Frame(self.scrollable_frame, bg='white', relief='solid', borderwidth=1)
        
        # Product info
        info_frame = tk.Frame(card, bg='white')
        info_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Name
        tk.Label(
            info_frame,
            text=product.name,
            font=(config.FONT_FAMILY, config.FONT_SIZE_MEDIUM, 'bold'),
            bg='white',
            fg=config.TEXT_COLOR,
            wraplength=200
        ).pack(anchor='w', pady=(0, 5))
        
        # Category
        tk.Label(
            info_frame,
            text=product.category,
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg='white',
            fg='gray'
        ).pack(anchor='w', pady=(0, 5))
        
        # Price
        tk.Label(
            info_frame,
            text=format_currency(product.price),
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR
        ).pack(anchor='w', pady=(10, 5))
        
        # Stock
        tk.Label(
            info_frame,
            text=f"In Stock: {product.stock_quantity}",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg='white',
            fg=config.SUCCESS_COLOR
        ).pack(anchor='w', pady=(0, 10))
        
        # Quantity selector
        qty_frame = tk.Frame(info_frame, bg='white')
        qty_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            qty_frame,
            text="Qty:",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        qty_var = tk.IntVar(value=1)
        qty_spinbox = tk.Spinbox(
            qty_frame,
            from_=1,
            to=product.stock_quantity,
            textvariable=qty_var,
            width=8,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            relief='solid',
            borderwidth=1
        )
        qty_spinbox.pack(side=tk.LEFT)
        
        # Add to cart button
        add_btn = tk.Button(
            info_frame,
            text="Add to Cart",
            command=lambda p=product, q=qty_var: self.add_to_cart(p, q.get()),
            **BUTTON_STYLE
        )
        add_btn.pack(fill=tk.X)
        
        return card
    
    def add_to_cart(self, product, quantity):
        if quantity < 1:
            show_error("Quantity must be at least 1")
            return
        
        if quantity > product.stock_quantity:
            show_error(f"Only {product.stock_quantity} items available in stock")
            return
        
        success, message = self.controllers['cart'].add_to_cart(
            self.user.user_id,
            product.product_id,
            quantity
        )
        
        if success:
            show_success(f"{quantity} x {product.name} added to cart")
            self.update_cart_callback()
        else:
            show_error(message)
    
    def search_products(self):
        query = self.search_entry.get().strip()
        
        # Clear products
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not query:
            self.load_products()
            return
        
        # Search products
        products = self.controllers['product'].search_products(query)
        
        # Display results
        row = 0
        col = 0
        max_cols = 3
        
        for product in products:
            if product.stock_quantity > 0:
                product_card = self.create_product_card(product)
                product_card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        for i in range(max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
