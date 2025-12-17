"""
Products View for Girlush Collections - Admin
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success, confirm, ProductDialog
from utils.helpers import format_currency

class ProductsView(tk.Frame):
    def __init__(self, parent, controllers):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controllers = controllers
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Products Management",
            **LABEL_TITLE_STYLE
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header_frame,
            text="+ Add Product",
            command=self.add_product,
            **BUTTON_STYLE
        ).pack(side=tk.RIGHT)
        
        # Search
        search_frame = tk.Frame(self, bg=config.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", **LABEL_STYLE).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, **ENTRY_STYLE, width=30)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        # Products table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'Category', 'Price', 'Cost', 'Stock'),
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Product Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Cost', text='Cost')
        self.tree.heading('Stock', text='Stock')
        
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=200)
        self.tree.column('Category', width=120)
        self.tree.column('Price', width=100)
        self.tree.column('Cost', width=100)
        self.tree.column('Stock', width=80)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Context menu
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Double-1>', lambda e: self.edit_product())
    
    def load_products(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get products
        products = self.controllers['product'].get_all_products()
        
        for product in products:
            self.tree.insert('', 'end', values=(
                product.product_id,
                product.name,
                product.category,
                format_currency(product.price),
                format_currency(product.cost),
                product.stock_quantity
            ))
    
    def search_products(self):
        query = self.search_entry.get().strip()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not query:
            self.load_products()
            return
        
        # Search products
        products = self.controllers['product'].search_products(query)
        
        for product in products:
            self.tree.insert('', 'end', values=(
                product.product_id,
                product.name,
                product.category,
                format_currency(product.price),
                format_currency(product.cost),
                product.stock_quantity
            ))
    
    def add_product(self):
        dialog = ProductDialog(self, "Add Product")
        result = dialog.show()
        
        if result:
            success, message = self.controllers['product'].create_product(
                name=result['name'],
                description=result['description'],
                category=result['category'],
                price=result['price'],
                cost=result['cost'],
                stock_quantity=result['stock_quantity']
            )
            
            if success:
                show_success(message)
                self.load_products()
            else:
                show_error(message)
    
    def edit_product(self):
        selection = self.tree.selection()
        if not selection:
            show_error("Please select a product to edit")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        
        product = self.controllers['product'].get_product(product_id)
        if not product:
            show_error("Product not found")
            return
        
        dialog = ProductDialog(self, "Edit Product", product)
        result = dialog.show()
        
        if result:
            success, message = self.controllers['product'].update_product(
                product_id=product_id,
                name=result['name'],
                description=result['description'],
                category=result['category'],
                price=result['price'],
                cost=result['cost'],
                stock_quantity=result['stock_quantity']
            )
            
            if success:
                show_success(message)
                self.load_products()
            else:
                show_error(message)
    
    def delete_product(self):
        selection = self.tree.selection()
        if not selection:
            show_error("Please select a product to delete")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        if confirm("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            success, message = self.controllers['product'].delete_product(product_id)
            
            if success:
                show_success(message)
                self.load_products()
            else:
                show_error(message)
    
    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Edit", command=self.edit_product)
        menu.add_command(label="Delete", command=self.delete_product)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
