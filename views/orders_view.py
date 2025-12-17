"""
Orders View for Girlush Collections
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success, confirm
from utils.helpers import format_currency, format_date_short, get_status_color

class OrdersView(tk.Frame):
    """Admin orders view"""
    def __init__(self, parent, controllers):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controllers = controllers
        
        self.create_widgets()
        self.load_orders()
    
    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text="Orders Management",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Orders table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Customer', 'Date', 'Total', 'Status', 'Payment'),
            show='headings',
            yscrollcommand=v_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Order ID')
        self.tree.heading('Customer', text='Customer')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Total', text='Total Amount')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Payment', text='Payment Method')
        
        self.tree.column('ID', width=80)
        self.tree.column('Customer', width=150)
        self.tree.column('Date', width=100)
        self.tree.column('Total', width=120)
        self.tree.column('Status', width=100)
        self.tree.column('Payment', width=120)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def load_orders(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get orders
        orders = self.controllers['order'].get_all_orders()
        
        for order in orders:
            self.tree.insert('', 'end', values=(
                order.get('order_id', ''),
                order.get('customer_name', 'N/A'),
                format_date_short(order.get('order_date', '')),
                format_currency(order.get('total_amount', 0)),
                order.get('status', '').upper(),
                order.get('payment_method', '')
            ), tags=(order.get('status', ''),))
    
    def show_context_menu(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Mark as Processing", command=lambda: self.update_status('processing'))
        menu.add_command(label="Mark as Completed", command=lambda: self.update_status('completed'))
        menu.add_command(label="Mark as Cancelled", command=lambda: self.update_status('cancelled'))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def update_status(self, new_status):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        order_id = item['values'][0]
        
        success, message = self.controllers['order'].update_order_status(order_id, new_status)
        
        if success:
            show_success(message)
            self.load_orders()
        else:
            show_error(message)

class CustomerOrdersView(tk.Frame):
    """Customer orders view"""
    def __init__(self, parent, user, controllers):
        super().__init__(parent, bg=config.BG_COLOR)
        self.user = user
        self.controllers = controllers
        
        self.create_widgets()
        self.load_orders()
    
    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text="My Orders",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Orders table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Date', 'Total', 'Status'),
            show='headings',
            yscrollcommand=v_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Order ID')
        self.tree.heading('Date', text='Order Date')
        self.tree.heading('Total', text='Total Amount')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=100)
        self.tree.column('Date', width=150)
        self.tree.column('Total', width=150)
        self.tree.column('Status', width=120)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_orders(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get user orders
        orders = self.controllers['order'].get_user_orders(self.user.user_id)
        
        for order in orders:
            self.tree.insert('', 'end', values=(
                order.get('order_id', ''),
                format_date_short(order.get('order_date', '')),
                format_currency(order.get('total_amount', 0)),
                order.get('status', '').upper()
            ))
