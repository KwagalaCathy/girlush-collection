"""
Dialog components for Girlush Collections
"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from assets.styles import *

def show_info(title: str, message: str):
    """Show information dialog"""
    messagebox.showinfo(title, message)

def show_success(message: str):
    """Show success dialog"""
    messagebox.showinfo("Success", message)

def show_error(message: str):
    """Show error dialog"""
    messagebox.showerror("Error", message)

def show_warning(message: str):
    """Show warning dialog"""
    messagebox.showwarning("Warning", message)

def confirm(title: str, message: str) -> bool:
    """Show confirmation dialog"""
    return messagebox.askyesno(title, message)

class InputDialog(tk.Toplevel):
    """Custom input dialog"""
    def __init__(self, parent, title: str, prompt: str, default: str = ""):
        super().__init__(parent)
        self.title(title)
        self.result = None
        
        # Configure window
        self.configure(bg=config.BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.geometry("400x150")
        window_width = 400
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create widgets
        frame = tk.Frame(self, bg=config.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        label = tk.Label(frame, text=prompt, **LABEL_STYLE)
        label.pack(anchor='w', pady=(0, 10))
        
        self.entry = tk.Entry(frame, **ENTRY_STYLE)
        self.entry.insert(0, default)
        self.entry.pack(fill=tk.X, pady=(0, 15))
        self.entry.select_range(0, tk.END)
        self.entry.focus()
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=config.BG_COLOR)
        btn_frame.pack()
        
        ok_btn = tk.Button(btn_frame, text="OK", command=self.on_ok, **BUTTON_STYLE)
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.on_cancel, 
                               **BUTTON_SECONDARY_STYLE)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind enter key
        self.entry.bind('<Return>', lambda e: self.on_ok())
        self.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()
    
    def on_cancel(self):
        self.result = None
        self.destroy()
    
    def show(self):
        self.wait_window()
        return self.result

class ProductDialog(tk.Toplevel):
    """Dialog for adding/editing products"""
    def __init__(self, parent, title: str, product=None, suppliers=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.product = product
        self.suppliers = suppliers or []
        
        # Configure window
        self.configure(bg=config.BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        window_width = 500
        window_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
        
        if product:
            self.populate_fields()
    
    def create_widgets(self):
        # Main container with canvas for scrolling
        main_container = tk.Frame(self, bg=config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(main_container, bg=config.BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=460)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Cleanup
        def on_destroy(event):
            canvas.unbind_all("<MouseWheel>")
        self.bind('<Destroy>', on_destroy)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
        
        frame = scrollable_frame
        
        # Name
        tk.Label(frame, text="Product Name:", **LABEL_STYLE).pack(anchor='w')
        self.name_entry = tk.Entry(frame, **ENTRY_STYLE)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        tk.Label(frame, text="Description:", **LABEL_STYLE).pack(anchor='w')
        self.desc_text = tk.Text(frame, height=4, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL))
        self.desc_text.pack(fill=tk.X, pady=(0, 10))
        
        # Category
        tk.Label(frame, text="Category:", **LABEL_STYLE).pack(anchor='w')
        self.category_entry = tk.Entry(frame, **ENTRY_STYLE)
        self.category_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Price
        tk.Label(frame, text="Price:", **LABEL_STYLE).pack(anchor='w')
        self.price_entry = tk.Entry(frame, **ENTRY_STYLE)
        self.price_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Cost
        tk.Label(frame, text="Cost:", **LABEL_STYLE).pack(anchor='w')
        self.cost_entry = tk.Entry(frame, **ENTRY_STYLE)
        self.cost_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Stock
        tk.Label(frame, text="Stock Quantity:", **LABEL_STYLE).pack(anchor='w')
        self.stock_entry = tk.Entry(frame, **ENTRY_STYLE)
        self.stock_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=config.BG_COLOR)
        btn_frame.pack(pady=15)
        
        save_btn = tk.Button(btn_frame, text="Save", command=self.on_save, **BUTTON_STYLE)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.on_cancel, 
                               **BUTTON_SECONDARY_STYLE)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def populate_fields(self):
        if self.product:
            self.name_entry.insert(0, self.product.name)
            self.desc_text.insert('1.0', self.product.description)
            self.category_entry.insert(0, self.product.category)
            self.price_entry.insert(0, str(self.product.price))
            self.cost_entry.insert(0, str(self.product.cost))
            self.stock_entry.insert(0, str(self.product.stock_quantity))
    
    def on_save(self):
        try:
            self.result = {
                'name': self.name_entry.get().strip(),
                'description': self.desc_text.get('1.0', tk.END).strip(),
                'category': self.category_entry.get().strip(),
                'price': float(self.price_entry.get()),
                'cost': float(self.cost_entry.get()),
                'stock_quantity': int(self.stock_entry.get())
            }
            self.destroy()
        except ValueError:
            show_error("Please enter valid numbers for price, cost, and stock")
    
    def on_cancel(self):
        self.result = None
        self.destroy()
    
    def show(self):
        self.wait_window()
        return self.result

class PaymentMethodDialog(tk.Toplevel):
    """Dialog for selecting payment method at checkout"""
    def __init__(self, parent, cart_items):
        super().__init__(parent)
        self.title("Select Payment Method")
        self.result = None
        self.cart_items = cart_items
        
        # Configure window
        self.configure(bg=config.BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        window_width = 450
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container with canvas for scrolling
        main_container = tk.Frame(self, bg=config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(main_container, bg=config.BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=430)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Cleanup
        def on_destroy(event):
            canvas.unbind_all("<MouseWheel>")
        self.bind('<Destroy>', on_destroy)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
        
        frame = scrollable_frame
        
        # Title
        tk.Label(
            frame,
            text="Select Payment Method",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg=config.BG_COLOR,
            fg=config.PRIMARY_COLOR
        ).pack(pady=(0, 10))
        
        tk.Label(
            frame,
            text="Payment will be made on delivery",
            font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
            bg=config.BG_COLOR,
            fg='gray'
        ).pack(pady=(0, 20))
        
        # Order summary
        summary_frame = tk.Frame(frame, bg='white', relief='solid', borderwidth=1)
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            summary_frame,
            text="Order Summary",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=15, pady=10)
        
        total = sum(item['price'] * item['quantity'] for item in self.cart_items)
        
        tk.Label(
            summary_frame,
            text=f"Total Items: {len(self.cart_items)}",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            bg='white'
        ).pack(anchor='w', padx=15, pady=2)
        
        tk.Label(
            summary_frame,
            text=f"Total Amount: UGX {total:,.0f}",
            font=(config.FONT_FAMILY, config.FONT_SIZE_MEDIUM, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR
        ).pack(anchor='w', padx=15, pady=(2, 10))
        
        # Payment methods
        tk.Label(
            frame,
            text="Choose Payment Method:",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
            bg=config.BG_COLOR
        ).pack(anchor='w', pady=(0, 10))
        
        self.payment_var = tk.StringVar(value='cash')
        
        payment_options = [
            ('cash', '💵 Cash on Delivery', 'Pay with cash when your order arrives'),
            ('card', '💳 Card on Delivery', 'Pay with card when your order arrives'),
            ('mobilemoney', '📱 Mobile Money', 'Pay via Mobile Money on delivery')
        ]
        
        for value, label, description in payment_options:
            radio_frame = tk.Frame(frame, bg='white', relief='solid', borderwidth=1, cursor='hand2')
            radio_frame.pack(fill=tk.X, pady=5)
            
            inner_frame = tk.Frame(radio_frame, bg='white')
            inner_frame.pack(fill=tk.X, padx=15, pady=10)
            
            radio = tk.Radiobutton(
                inner_frame,
                text=label,
                variable=self.payment_var,
                value=value,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                bg='white',
                activebackground='white',
                cursor='hand2'
            )
            radio.pack(anchor='w')
            
            tk.Label(
                inner_frame,
                text=description,
                font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
                bg='white',
                fg='gray'
            ).pack(anchor='w', padx=20)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=config.BG_COLOR)
        btn_frame.pack(pady=15)
        
        confirm_btn = tk.Button(
            btn_frame,
            text="Confirm Order",
            command=self.on_confirm_payment,
            **BUTTON_SUCCESS_STYLE
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.on_cancel_payment,
            **BUTTON_SECONDARY_STYLE
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def on_confirm_payment(self):
        self.result = {
            'payment_method': self.payment_var.get()
        }
        self.destroy()
    
    def on_cancel_payment(self):
        self.result = None
        self.destroy()
    
    def show(self):
        self.wait_window()
        return self.result


class QuantityDialog(tk.Toplevel):
    """Dialog for updating cart item quantity"""
    def __init__(self, parent, product_name, current_quantity):
        super().__init__(parent)
        self.title("Update Quantity")
        self.result = None
        self.product_name = product_name
        self.current_quantity = current_quantity
        
        # Configure window
        self.configure(bg=config.BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        window_width = 350
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
        self.wait_window()
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self, bg='white', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            main_frame,
            text="Update Quantity",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR
        ).pack(pady=(0, 10))
        
        # Product name
        tk.Label(
            main_frame,
            text=f"Product: {self.product_name}",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            bg='white',
            fg=config.TEXT_COLOR
        ).pack(pady=(0, 20))
        
        # Quantity input
        qty_frame = tk.Frame(main_frame, bg='white')
        qty_frame.pack(pady=(0, 20))
        
        tk.Label(
            qty_frame,
            text="New Quantity:",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.qty_var = tk.IntVar(value=self.current_quantity)
        self.qty_spinbox = tk.Spinbox(
            qty_frame,
            from_=1,
            to=999,
            textvariable=self.qty_var,
            width=10,
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            relief='solid',
            borderwidth=1
        )
        self.qty_spinbox.pack(side=tk.LEFT)
        self.qty_spinbox.focus()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack()
        
        tk.Button(
            button_frame,
            text="Update",
            **BUTTON_PRIMARY_STYLE,
            command=self.on_update
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            **BUTTON_SECONDARY_STYLE,
            command=self.on_cancel
        ).pack(side=tk.LEFT, padx=5)
    
    def on_update(self):
        try:
            quantity = int(self.qty_var.get())
            if quantity < 1:
                messagebox.showerror("Error", "Quantity must be at least 1")
                return
            self.result = quantity
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def on_cancel(self):
        self.result = None
        self.destroy()


class SupplierDialog(tk.Toplevel):
    """Dialog for adding/editing suppliers"""
    def __init__(self, parent, supplier=None):
        super().__init__(parent)
        self.title("Edit Supplier" if supplier else "Add Supplier")
        self.result = None
        self.supplier = supplier
        
        # Configure window
        self.configure(bg=config.BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center window
        window_width = 450
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
        self.wait_window()
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self, bg='white', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        tk.Label(
            main_frame,
            text="Edit Supplier" if self.supplier else "Add New Supplier",
            font=(config.FONT_FAMILY, config.FONT_SIZE_XLARGE, 'bold'),
            bg='white',
            fg=config.PRIMARY_COLOR
        ).pack(pady=(0, 20))
        
        # Form fields
        fields = [
            ("Supplier Name:", "name"),
            ("Contact Person:", "contact_person"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("Address:", "address"),
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            field_frame = tk.Frame(main_frame, bg='white')
            field_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                field_frame,
                text=label_text,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                bg='white',
                fg=config.TEXT_COLOR,
                anchor='w'
            ).pack(fill=tk.X)
            
            entry = tk.Entry(
                field_frame,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                relief='solid',
                borderwidth=1
            )
            entry.pack(fill=tk.X, pady=(5, 0))
            
            if self.supplier and field_name in self.supplier:
                entry.insert(0, self.supplier[field_name])
            
            self.entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="Save",
            **BUTTON_PRIMARY_STYLE,
            command=self.on_save
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            **BUTTON_SECONDARY_STYLE,
            command=self.on_cancel
        ).pack(side=tk.LEFT, padx=5)
    
    def on_save(self):
        # Validate
        name = self.entries['name'].get().strip()
        contact_person = self.entries['contact_person'].get().strip()
        email = self.entries['email'].get().strip()
        phone = self.entries['phone'].get().strip()
        address = self.entries['address'].get().strip()
        
        if not name:
            messagebox.showerror("Error", "Supplier name is required")
            return
        
        if not contact_person:
            messagebox.showerror("Error", "Contact person is required")
            return
        
        if not email:
            messagebox.showerror("Error", "Email is required")
            return
        
        self.result = {
            'name': name,
            'contact_person': contact_person,
            'email': email,
            'phone': phone,
            'address': address
        }
        self.destroy()
    
    def on_cancel(self):
        self.result = None
        self.destroy()
