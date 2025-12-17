"""
Sales View for Girlush Collections - Admin
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from utils.helpers import format_currency, format_date_short

class SalesView(tk.Frame):
    def __init__(self, parent, controllers):
        super().__init__(parent, bg=config.BG_COLOR)
        self.controllers = controllers
        
        self.create_widgets()
        self.load_sales()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Sales Reports",
            **LABEL_TITLE_STYLE
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header_frame,
            text="📊 Generate Report",
            **BUTTON_PRIMARY_STYLE,
            command=self.generate_report
        ).pack(side=tk.RIGHT)
        
        # Summary cards
        summary_frame = tk.Frame(self, bg=config.BG_COLOR)
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.total_sales_label = tk.Label(
            summary_frame,
            text="Total Sales: ₱0.00",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR,
            relief='solid',
            borderwidth=1,
            padx=20,
            pady=15
        )
        self.total_sales_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        self.total_orders_label = tk.Label(
            summary_frame,
            text="Total Orders: 0",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white',
            fg=config.SUCCESS_COLOR,
            relief='solid',
            borderwidth=1,
            padx=20,
            pady=15
        )
        self.total_orders_label.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Sales table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('Date', 'Orders', 'Total Sales'),
            show='headings',
            yscrollcommand=v_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('Date', text='Date')
        self.tree.heading('Orders', text='Number of Orders')
        self.tree.heading('Total Sales', text='Total Sales')
        
        self.tree.column('Date', width=150)
        self.tree.column('Orders', width=150)
        self.tree.column('Total Sales', width=150)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_sales(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get sales data
        sales_data = self.controllers['db'].get_sales_data()
        
        total_sales = 0
        total_orders = 0
        
        for sale in sales_data:
            self.tree.insert('', 'end', values=(
                format_date_short(sale.get('date', '')),
                sale.get('order_count', 0),
                format_currency(sale.get('total_sales', 0))
            ))
            
            total_sales += sale.get('total_sales', 0)
            total_orders += sale.get('order_count', 0)
        
        # Update summary
        self.total_sales_label.config(text=f"Total Sales: {format_currency(total_sales)}")
        self.total_orders_label.config(text=f"Total Orders: {total_orders}")
    
    def generate_report(self):
        """Generate detailed sales report"""
        from tkinter import messagebox
        import datetime
        
        # Get all orders
        orders = self.controllers['order'].get_all_orders()
        
        if not orders:
            messagebox.showinfo("Sales Report", "No sales data available to generate report.")
            return
        
        # Calculate statistics
        total_revenue = sum(order.get('total_amount', 0) for order in orders)
        total_orders = len(orders)
        completed_orders = len([o for o in orders if o.get('status') == 'completed'])
        pending_orders = len([o for o in orders if o.get('status') == 'pending'])
        
        # Payment method breakdown
        payment_methods = {}
        for order in orders:
            method = order.get('payment_method', 'Unknown')
            payment_methods[method] = payment_methods.get(method, 0) + 1
        
        # Create report dialog
        report_window = tk.Toplevel(self)
        report_window.title("Sales Report")
        report_window.geometry("600x500")
        report_window.configure(bg='white')
        
        # Center window
        report_window.transient(self)
        report_window.grab_set()
        
        # Report content
        content_frame = tk.Frame(report_window, bg='white', padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            content_frame,
            text="Sales Report Summary",
            font=(config.FONT_FAMILY, 20, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR
        ).pack(pady=(0, 20))
        
        # Date
        tk.Label(
            content_frame,
            text=f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg='white',
            fg='gray'
        ).pack(pady=(0, 20))
        
        # Statistics
        stats_data = [
            ("Total Revenue:", format_currency(total_revenue)),
            ("Total Orders:", str(total_orders)),
            ("Completed Orders:", str(completed_orders)),
            ("Pending Orders:", str(pending_orders)),
            ("Average Order Value:", format_currency(total_revenue / total_orders if total_orders > 0 else 0))
        ]
        
        for label, value in stats_data:
            row = tk.Frame(content_frame, bg='white')
            row.pack(fill=tk.X, pady=8)
            
            tk.Label(
                row,
                text=label,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                bg='white',
                anchor='w',
                width=25
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row,
                text=value,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                bg='white',
                fg=config.PRIMARY_COLOR,
                anchor='e'
            ).pack(side=tk.RIGHT)
        
        # Payment Methods
        tk.Label(
            content_frame,
            text="Payment Methods Breakdown:",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(20, 10))
        
        for method, count in payment_methods.items():
            percentage = (count / total_orders * 100) if total_orders > 0 else 0
            tk.Label(
                content_frame,
                text=f"  • {method.title()}: {count} orders ({percentage:.1f}%)",
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                bg='white'
            ).pack(anchor='w', pady=2)
        
        # Close button
        tk.Button(
            content_frame,
            text="Close",
            **BUTTON_SECONDARY_STYLE,
            command=report_window.destroy
        ).pack(pady=(30, 0))
