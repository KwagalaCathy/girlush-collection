"""
Customers View for Girlush Collections - Admin
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from utils.helpers import format_date_short

class CustomersView(tk.Frame):
    def __init__(self, parent, controllers):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controllers = controllers
        
        self.create_widgets()
        self.load_customers()
    
    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text="Customers Management",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Customers table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'Email', 'Phone', 'City', 'Registered'),
            show='headings',
            yscrollcommand=v_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('City', text='City')
        self.tree.heading('Registered', text='Registered')
        
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=150)
        self.tree.column('Email', width=200)
        self.tree.column('Phone', width=120)
        self.tree.column('City', width=100)
        self.tree.column('Registered', width=100)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_customers(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get customers
        customers = self.controllers['customer'].get_all_customers()
        
        for customer in customers:
            self.tree.insert('', 'end', values=(
                customer.get('customer_id', ''),
                customer.get('name', ''),
                customer.get('email', ''),
                customer.get('phone', ''),
                customer.get('city', ''),
                format_date_short(customer.get('created_at', ''))
            ))
