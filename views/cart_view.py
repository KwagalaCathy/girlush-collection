"""
Cart View for Girlush Collections - Customer
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *
from components.dialogs import show_error, show_success, confirm, PaymentMethodDialog
from utils.helpers import format_currency

class CartView(tk.Frame):
    def __init__(self, parent, user, controllers, update_cart_callback):
        super().__init__(parent, bg=config.BG_COLOR)
        self.user = user
        self.controllers = controllers
        self.update_cart_callback = update_cart_callback
        
        self.create_widgets()
        self.load_cart()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Shopping Cart",
            **LABEL_TITLE_STYLE
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header_frame,
            text="Clear Cart",
            command=self.clear_cart,
            **BUTTON_DANGER_STYLE
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            header_frame,
            text="Checkout",
            command=self.checkout,
            **BUTTON_SUCCESS_STYLE
        ).pack(side=tk.RIGHT)
        
        # Cart items table
        table_frame = tk.Frame(self, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Product', 'Price', 'Quantity', 'Subtotal'),
            show='headings',
            yscrollcommand=v_scrollbar.set
        )
        
        v_scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Cart ID')
        self.tree.heading('Product', text='Product Name')
        self.tree.heading('Price', text='Unit Price')
        self.tree.heading('Quantity', text='Quantity')
        self.tree.heading('Subtotal', text='Subtotal')
        
        self.tree.column('ID', width=80)
        self.tree.column('Product', width=200)
        self.tree.column('Price', width=100)
        self.tree.column('Quantity', width=100)
        self.tree.column('Subtotal', width=120)
        
        # Pack
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Total frame
        total_frame = tk.Frame(self, bg='white', relief='solid', borderwidth=1)
        total_frame.pack(fill=tk.X, pady=10)
        
        inner_frame = tk.Frame(total_frame, bg='white')
        inner_frame.pack(padx=20, pady=15)
        
        tk.Label(
            inner_frame,
            text="Total:",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        self.total_label = tk.Label(
            inner_frame,
            text=format_currency(0),
            font=(config.FONT_FAMILY, config.FONT_SIZE_XLARGE, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR
        )
        self.total_label.pack(side=tk.LEFT)
    
    def load_cart(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get cart items
        cart_items = self.controllers['cart'].get_cart_items(self.user.user_id)
        
        total = 0
        for item in cart_items:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            
            self.tree.insert('', 'end', values=(
                item['cart_id'],
                item['name'],
                format_currency(item['price']),
                item['quantity'],
                format_currency(subtotal)
            ))
        
        self.total_label.config(text=format_currency(total))
        self.update_cart_callback()
    
    def show_context_menu(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Update Quantity", command=self.update_quantity)
        menu.add_separator()
        menu.add_command(label="Remove from Cart", command=self.remove_item)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def update_quantity(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        cart_id = item['values'][0]
        product_name = item['values'][1]
        current_qty = item['values'][3]
        
        from components.dialogs import QuantityDialog
        dialog = QuantityDialog(self, product_name, current_qty)
        
        if dialog.result:
            new_quantity = dialog.result
            success, message = self.controllers['cart'].update_cart_quantity(cart_id, new_quantity)
            
            if success:
                show_success("Quantity updated successfully")
                self.load_cart()
            else:
                show_error(message)
    
    def remove_item(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        cart_id = item['values'][0]
        
        success, message = self.controllers['cart'].remove_from_cart(cart_id)
        
        if success:
            show_success(message)
            self.load_cart()
        else:
            show_error(message)
    
    def clear_cart(self):
        if not confirm("Clear Cart", "Are you sure you want to clear your cart?"):
            return
        
        success, message = self.controllers['cart'].clear_cart(self.user.user_id)
        
        if success:
            show_success(message)
            self.load_cart()
        else:
            show_error(message)
    
    def checkout(self):
        cart_items = self.controllers['cart'].get_cart_items(self.user.user_id)
        
        if not cart_items:
            show_error("Your cart is empty")
            return
        
        # Show payment method selection dialog
        payment_dialog = PaymentMethodDialog(self, cart_items)
        result = payment_dialog.show()
        
        if not result:
            return  # User cancelled
        
        payment_method = result['payment_method']
        
        # Get customer info
        customer = self.controllers['customer'].get_customer_by_user_id(self.user.user_id)
        customer_id = customer.customer_id if customer else None
        
        # Create order with pay on delivery
        success, message, order_id = self.controllers['order'].create_order(
            user_id=self.user.user_id,
            customer_id=customer_id,
            cart_items=cart_items,
            payment_method=payment_method,
            shipping_address=customer.address if customer else ''
        )
        
        if success:
            show_success(f"Order #{order_id} placed successfully!\nPayment: {payment_method.upper()} (Pay on Delivery)")
            self.load_cart()
        else:
            show_error(message)
