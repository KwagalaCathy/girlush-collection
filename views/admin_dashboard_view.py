"""
Admin Dashboard View for Girlush Collections
"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from assets.styles import *
from utils.helpers import format_currency
from components.dialogs import show_info

class AdminDashboardView(tk.Frame):
    def __init__(self, parent, user, controllers, on_logout):
        super().__init__(parent, bg=config.BG_COLOR)
        self.user = user
        self.controllers = controllers
        self.on_logout = on_logout
        self.current_view = None
        
        self.create_widgets()
        self.load_dashboard()
    
    def create_widgets(self):
        # Top bar
        top_bar = tk.Frame(self, bg=config.PRIMARY_COLOR, height=60)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        tk.Label(
            top_bar,
            text=config.APP_NAME,
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            fg='white',
            bg=config.PRIMARY_COLOR
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            top_bar,
            text=f"Welcome, {self.user.name} (Admin)",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            fg='white',
            bg=config.PRIMARY_COLOR
        ).pack(side=tk.RIGHT, padx=20)
        
        # Main container
        main_container = tk.Frame(self, bg=config.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_container, bg='#2C3E50', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Menu items
        menu_items = [
            ("Dashboard", self.load_dashboard),
            ("Products", self.load_products),
            ("Customers", self.load_customers),
            ("Orders", self.load_orders),
            ("Suppliers", self.load_suppliers),
            ("Sales Reports", self.load_sales),
            ("Settings", self.load_settings),
            ("Logout", self.on_logout)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                bg='#2C3E50',
                fg='white',
                relief='flat',
                anchor='w',
                padx=20,
                pady=15,
                cursor='hand2',
                command=command
            )
            btn.pack(fill=tk.X)
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#34495E'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#2C3E50'))
        
        # Content area with scrolling
        content_container = tk.Frame(main_container, bg=config.BG_COLOR)
        content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(content_container, bg=config.BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(content_container, orient='vertical', command=canvas.yview)
        self.content_area = tk.Frame(canvas, bg=config.BG_COLOR)
        
        self.content_area.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.content_area, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind canvas resize to expand content width
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
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
    
    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def load_dashboard(self):
        self.clear_content()
        
        tk.Label(
            self.content_area,
            text="Admin Dashboard",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Get stats
        stats = self.controllers['db'].get_dashboard_stats()
        
        # Quick Actions
        tk.Label(
            self.content_area,
            text="Quick Actions",
            **LABEL_HEADING_STYLE
        ).pack(anchor='w', pady=(10, 10))
        
        actions_frame = tk.Frame(self.content_area, bg=config.BG_COLOR)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        quick_actions = [
            ("Add Product", "➕", self.load_products, config.SUCCESS_COLOR),
            ("View Orders", "📦", self.load_orders, config.INFO_COLOR),
            ("Sales Report", "📊", self.load_sales, config.PRIMARY_COLOR),
            ("Manage Users", "👥", self.load_customers, config.WARNING_COLOR),
        ]
        
        for i, (title, icon, command, color) in enumerate(quick_actions):
            action_card = tk.Frame(actions_frame, bg='white', relief='solid', borderwidth=1, cursor='hand2')
            action_card.grid(row=0, column=i, padx=10, sticky='ew')
            actions_frame.columnconfigure(i, weight=1)
            
            card_content = tk.Frame(action_card, bg='white')
            card_content.pack(pady=15, padx=15)
            
            tk.Label(
                card_content,
                text=icon,
                font=(config.FONT_FAMILY, 24),
                bg='white'
            ).pack()
            
            tk.Label(
                card_content,
                text=title,
                font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL, 'bold'),
                bg='white',
                fg=color
            ).pack(pady=(5, 0))
            
            action_card.bind('<Button-1>', lambda e, cmd=command: cmd())
            for child in action_card.winfo_children():
                child.bind('<Button-1>', lambda e, cmd=command: cmd())
        
        # Stats cards
        tk.Label(
            self.content_area,
            text="Overview Statistics",
            **LABEL_HEADING_STYLE
        ).pack(anchor='w', pady=(20, 10))
        
        cards_frame = tk.Frame(self.content_area, bg=config.BG_COLOR)
        cards_frame.pack(fill=tk.X, pady=10)
        
        stats_data = [
            ("Total Products", stats.get('total_products', 0), config.INFO_COLOR),
            ("Total Customers", stats.get('total_customers', 0), config.SUCCESS_COLOR),
            ("Total Orders", stats.get('total_orders', 0), config.WARNING_COLOR),
            ("Total Sales", format_currency(stats.get('total_sales', 0)), config.PRIMARY_COLOR)
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            card = tk.Frame(cards_frame, bg='white', relief='solid', borderwidth=1)
            card.grid(row=0, column=i, padx=10, sticky='ew')
            cards_frame.columnconfigure(i, weight=1)
            
            tk.Label(
                card,
                text=str(value),
                font=(config.FONT_FAMILY, 24, 'bold'),
                fg=color,
                bg='white'
            ).pack(pady=(20, 5))
            
            tk.Label(
                card,
                text=label,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                fg=config.TEXT_COLOR,
                bg='white'
            ).pack(pady=(0, 20))
        
        # Recent Orders
        tk.Label(
            self.content_area,
            text="Recent Orders",
            **LABEL_HEADING_STYLE
        ).pack(anchor='w', pady=(20, 10))
        
        orders_frame = tk.Frame(self.content_area, bg='white', relief='solid', borderwidth=1)
        orders_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        recent_orders = self.controllers['order'].get_all_orders()[:10]
        
        if recent_orders:
            for order in recent_orders:
                order_frame = tk.Frame(orders_frame, bg='white')
                order_frame.pack(fill=tk.X, padx=20, pady=8)
                
                tk.Label(
                    order_frame,
                    text=f"Order #{order.get('order_id')} - {order.get('customer_name', 'N/A')}",
                    font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                    bg='white'
                ).pack(side=tk.LEFT)
                
                status_color = {'pending': config.WARNING_COLOR, 'completed': config.SUCCESS_COLOR, 
                               'processing': config.INFO_COLOR, 'cancelled': config.DANGER_COLOR}.get(order.get('status', ''), config.TEXT_COLOR)
                
                tk.Label(
                    order_frame,
                    text=order.get('status', '').upper(),
                    font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL, 'bold'),
                    bg='white',
                    fg=status_color
                ).pack(side=tk.RIGHT, padx=10)
                
                tk.Label(
                    order_frame,
                    text=format_currency(order.get('total_amount', 0)),
                    font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                    bg='white',
                    fg=config.PRIMARY_COLOR
                ).pack(side=tk.RIGHT)
        else:
            tk.Label(
                orders_frame,
                text="No orders yet",
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                bg='white',
                fg='gray'
            ).pack(pady=40)
        
        # Alerts
        low_stock = stats.get('low_stock_products', 0)
        pending = stats.get('pending_orders', 0)
        
        if low_stock > 0 or pending > 0:
            tk.Label(
                self.content_area,
                text="Alerts",
                **LABEL_HEADING_STYLE
            ).pack(anchor='w', pady=(20, 10))
            
            alerts_frame = tk.Frame(self.content_area, bg='white', relief='solid', borderwidth=1)
            alerts_frame.pack(fill=tk.X, pady=10)
            
            if low_stock > 0:
                alert = tk.Label(
                    alerts_frame,
                    text=f"⚠ {low_stock} products are running low on stock",
                    font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                    bg='white',
                    fg=config.WARNING_COLOR
                )
                alert.pack(anchor='w', padx=20, pady=10)
            
            if pending > 0:
                alert = tk.Label(
                    alerts_frame,
                    text=f"📦 {pending} orders are pending processing",
                    font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                    bg='white',
                    fg=config.INFO_COLOR
                )
                alert.pack(anchor='w', padx=20, pady=10)
    
    def load_products(self):
        from views.products_view import ProductsView
        self.clear_content()
        ProductsView(self.content_area, self.controllers).pack(fill=tk.BOTH, expand=True)
    
    def load_customers(self):
        from views.customers_view import CustomersView
        self.clear_content()
        CustomersView(self.content_area, self.controllers).pack(fill=tk.BOTH, expand=True)
    
    def load_orders(self):
        from views.orders_view import OrdersView
        self.clear_content()
        OrdersView(self.content_area, self.controllers).pack(fill=tk.BOTH, expand=True)
    
    def load_sales(self):
        from views.sales_view import SalesView
        self.clear_content()
        SalesView(self.content_area, self.controllers)
    
    def load_suppliers(self):
        self.clear_content()
        
        tk.Label(
            self.content_area,
            text="Suppliers Management",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Add Supplier Button
        btn_frame = tk.Frame(self.content_area, bg=config.BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=10)
        
        add_btn = tk.Button(
            btn_frame,
            text="+ Add New Supplier",
            **BUTTON_PRIMARY_STYLE,
            command=self.add_supplier
        )
        add_btn.pack(side=tk.LEFT)
        
        # Suppliers Table
        table_frame = tk.Frame(self.content_area, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(table_frame, bg=config.PRIMARY_COLOR)
        header_frame.pack(fill=tk.X)
        
        headers = ["ID", "Name", "Contact Person", "Email", "Phone", "Actions"]
        weights = [1, 3, 2, 3, 2, 2]
        
        for i, (header, weight) in enumerate(zip(headers, weights)):
            header_label = tk.Label(
                header_frame,
                text=header,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                bg=config.PRIMARY_COLOR,
                fg='white',
                anchor='w'
            )
            header_label.grid(row=0, column=i, padx=10, pady=10, sticky='ew')
            header_frame.columnconfigure(i, weight=weight)
        
        # Scrollable content
        canvas = tk.Canvas(table_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(table_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Data Rows
        suppliers = self.controllers['db'].get_all_suppliers()
        
        for idx, supplier in enumerate(suppliers):
            row_bg = 'white' if idx % 2 == 0 else '#f8f9fa'
            row_frame = tk.Frame(scrollable_frame, bg=row_bg)
            row_frame.pack(fill=tk.X, pady=1)
            
            values = [
                supplier['supplier_id'],
                supplier['name'],
                supplier['contact_person'],
                supplier['email'],
                supplier['phone'],
                ""
            ]
            
            for i, (value, weight) in enumerate(zip(values, weights)):
                if i < len(values) - 1:
                    tk.Label(
                        row_frame,
                        text=value,
                        font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                        bg=row_bg,
                        anchor='w'
                    ).grid(row=0, column=i, padx=10, pady=10, sticky='ew')
                    row_frame.columnconfigure(i, weight=weight)
            
            # Action buttons
            action_frame = tk.Frame(row_frame, bg=row_bg)
            action_frame.grid(row=0, column=len(values)-1, padx=10, pady=5, sticky='ew')
            row_frame.columnconfigure(len(values)-1, weight=weights[-1])
            
            edit_btn = tk.Button(
                action_frame,
                text="✏ Edit",
                **BUTTON_SECONDARY_STYLE,
                command=lambda s=supplier: self.edit_supplier(s)
            )
            edit_btn.pack(side=tk.LEFT, padx=2)
            
            delete_btn = tk.Button(
                action_frame,
                text="🗑 Delete",
                bg=config.DANGER_COLOR,
                fg='white',
                font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
                relief='flat',
                cursor='hand2',
                command=lambda s=supplier: self.delete_supplier(s)
            )
            delete_btn.pack(side=tk.LEFT, padx=2)
    
    def add_supplier(self):
        from components.dialogs import SupplierDialog
        dialog = SupplierDialog(self.master, None)
        if dialog.result:
            self.controllers['db'].create_supplier(**dialog.result)
            messagebox.showinfo("Success", "Supplier added successfully!")
            self.load_suppliers()
    
    def edit_supplier(self, supplier):
        from components.dialogs import SupplierDialog
        dialog = SupplierDialog(self.master, supplier)
        if dialog.result:
            self.controllers['db'].update_supplier(supplier['supplier_id'], **dialog.result)
            messagebox.showinfo("Success", "Supplier updated successfully!")
            self.load_suppliers()
    
    def delete_supplier(self, supplier):
        if messagebox.askyesno("Confirm", f"Delete supplier '{supplier['name']}'?"):
            self.controllers['db'].delete_supplier(supplier['supplier_id'])
            messagebox.showinfo("Success", "Supplier deleted successfully!")
            self.load_suppliers()
    
    def load_settings(self):
        self.clear_content()
        
        tk.Label(
            self.content_area,
            text="Application Settings",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Settings Container
        settings_frame = tk.Frame(self.content_area, bg='white', relief='solid', borderwidth=1)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Business Information
        tk.Label(
            settings_frame,
            text="Business Information",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=15)
        
        business_settings = [
            ("Business Name:", "Girlush Collections"),
            ("Address:", "Kampala, Uganda"),
            ("Phone:", "+256 XXX XXXXXX"),
            ("Email:", "info@girlushcollections.com"),
        ]
        
        for label_text, value in business_settings:
            setting_frame = tk.Frame(settings_frame, bg='white')
            setting_frame.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(
                setting_frame,
                text=label_text,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                bg='white',
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            entry = tk.Entry(
                setting_frame,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                relief='solid',
                borderwidth=1
            )
            entry.insert(0, value)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Frame(settings_frame, height=2, bg='#e0e0e0').pack(fill=tk.X, padx=20, pady=20)
        
        # Application Settings
        tk.Label(
            settings_frame,
            text="Application Settings",
            font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, 'bold'),
            bg='white'
        ).pack(anchor='w', padx=20, pady=15)
        
        app_settings = [
            ("Currency:", "UGX (Ugandan Shillings)"),
            ("Low Stock Threshold:", "10 units"),
            ("Tax Rate:", "18%"),
            ("Default Payment Method:", "Pay on Delivery"),
        ]
        
        for label_text, value in app_settings:
            setting_frame = tk.Frame(settings_frame, bg='white')
            setting_frame.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(
                setting_frame,
                text=label_text,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                bg='white',
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            entry = tk.Entry(
                setting_frame,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                relief='solid',
                borderwidth=1
            )
            entry.insert(0, value)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Frame(settings_frame, height=2, bg='#e0e0e0').pack(fill=tk.X, padx=20, pady=20)
        
        # Save Button
        save_btn = tk.Button(
            settings_frame,
            text="Save Settings",
            **BUTTON_PRIMARY_STYLE,
            command=lambda: messagebox.showinfo("Info", "Settings saved successfully!")
        )
        save_btn.pack(pady=20).pack(fill=tk.BOTH, expand=True)
