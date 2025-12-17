"""
Customer Dashboard View for Girlush Collections
"""
import tkinter as tk
from tkinter import ttk
import config
from assets.styles import *

class CustomerDashboardView(tk.Frame):
    def __init__(self, parent, user, controllers, on_logout):
        super().__init__(parent, bg=config.BG_COLOR)
        self.user = user
        self.controllers = controllers
        self.on_logout = on_logout
        
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
        
        # Cart icon
        cart_count = self.controllers['cart'].get_cart_count(self.user.user_id)
        self.cart_label = tk.Label(
            top_bar,
            text=f"🛒 Cart ({cart_count})",
            font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
            fg='white',
            bg=config.PRIMARY_COLOR,
            cursor='hand2'
        )
        self.cart_label.pack(side=tk.RIGHT, padx=20)
        self.cart_label.bind('<Button-1>', lambda e: self.load_cart())
        
        tk.Label(
            top_bar,
            text=f"Welcome, {self.user.name}",
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
            ("Shop", self.load_shop),
            ("My Cart", self.load_cart),
            ("My Orders", self.load_orders),
            ("Profile", self.load_profile),
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
    
    def update_cart_count(self):
        cart_count = self.controllers['cart'].get_cart_count(self.user.user_id)
        self.cart_label.config(text=f"🛒 Cart ({cart_count})")
    
    def load_dashboard(self):
        """Load customer dashboard with quick actions and stats"""
        self.clear_content()
        
        # Dashboard title
        tk.Label(
            self.content_area,
            text="Dashboard",
            **LABEL_TITLE_STYLE
        ).pack(anchor='w', pady=(0, 20))
        
        # Quick Actions Section
        tk.Label(
            self.content_area,
            text="Quick Actions",
            **LABEL_HEADING_STYLE
        ).pack(anchor='w', pady=(10, 10))
        
        actions_frame = tk.Frame(self.content_area, bg=config.BG_COLOR)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        quick_actions = [
            ("My Orders", "📦", self.load_orders, config.INFO_COLOR),
            ("My Cart", "🛒", self.load_cart, config.PRIMARY_COLOR),
            ("Profile Settings", "⚙️", self.load_profile, config.SUCCESS_COLOR),
        ]
        
        for i, (title, icon, command, color) in enumerate(quick_actions):
            action_card = tk.Frame(actions_frame, bg='white', relief='solid', borderwidth=1, cursor='hand2')
            action_card.grid(row=0, column=i, padx=10, sticky='ew')
            actions_frame.columnconfigure(i, weight=1)
            
            card_content = tk.Frame(action_card, bg='white')
            card_content.pack(pady=20, padx=20)
            
            tk.Label(
                card_content,
                text=icon,
                font=(config.FONT_FAMILY, 32),
                bg='white'
            ).pack()
            
            tk.Label(
                card_content,
                text=title,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                bg='white',
                fg=color
            ).pack(pady=(5, 0))
            
            action_card.bind('<Button-1>', lambda e, cmd=command: cmd())
            for child in action_card.winfo_children():
                child.bind('<Button-1>', lambda e, cmd=command: cmd())
        
        # Quick Stats
        tk.Label(
            self.content_area,
            text="Quick Stats",
            **LABEL_HEADING_STYLE
        ).pack(anchor='w', pady=(20, 10))
        
        stats_frame = tk.Frame(self.content_area, bg=config.BG_COLOR)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Get user stats
        orders = self.controllers['order'].get_user_orders(self.user.user_id)
        cart_count = self.controllers['cart'].get_cart_count(self.user.user_id)
        total_spent = sum(o.get('total_amount', 0) for o in orders if o.get('status') == 'completed')
        
        stats_data = [
            ("Total Orders", len(orders), config.INFO_COLOR),
            ("Cart Items", cart_count, config.PRIMARY_COLOR),
            ("Total Spent", f"UGX {total_spent:,.0f}", config.SUCCESS_COLOR)
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            stat_card = tk.Frame(stats_frame, bg='white', relief='solid', borderwidth=1)
            stat_card.grid(row=0, column=i, padx=10, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(
                stat_card,
                text=str(value),
                font=(config.FONT_FAMILY, 24, 'bold'),
                fg=color,
                bg='white'
            ).pack(pady=(20, 5))
            
            tk.Label(
                stat_card,
                text=label,
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                fg=config.TEXT_COLOR,
                bg='white'
            ).pack(pady=(0, 20))
        
        # Recent Activities
        tk.Label(
            self.content_area,
            text="Recent Orders",
            **LABEL_HEADING_STYLE
        ).pack(anchor='w', pady=(20, 10))
        
        activities_frame = tk.Frame(self.content_area, bg='white', relief='solid', borderwidth=1)
        activities_frame.pack(fill=tk.BOTH, expand=True)
        
        if orders:
            # Show last 5 orders
            for order in orders[:5]:
                order_frame = tk.Frame(activities_frame, bg='white')
                order_frame.pack(fill=tk.X, padx=20, pady=10)
                
                tk.Label(
                    order_frame,
                    text=f"Order #{order.get('order_id')}",
                    font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, 'bold'),
                    bg='white'
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    order_frame,
                    text=f"UGX {order.get('total_amount', 0):,.0f}",
                    font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                    bg='white',
                    fg=config.PRIMARY_COLOR
                ).pack(side=tk.RIGHT, padx=20)
                
                status_color = {'pending': config.WARNING_COLOR, 'completed': config.SUCCESS_COLOR, 
                               'processing': config.INFO_COLOR, 'cancelled': config.DANGER_COLOR}.get(order.get('status', ''), config.TEXT_COLOR)
                
                tk.Label(
                    order_frame,
                    text=order.get('status', '').upper(),
                    font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL),
                    bg='white',
                    fg=status_color
                ).pack(side=tk.RIGHT)
        else:
            tk.Label(
                activities_frame,
                text="No orders yet. Start shopping!",
                font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL),
                bg='white',
                fg='gray'
            ).pack(pady=40)
    
    def load_shop(self):
        from views.shop_view import ShopView
        self.clear_content()
        ShopView(self.content_area, self.user, self.controllers, self.update_cart_count).pack(fill=tk.BOTH, expand=True)
    
    def load_cart(self):
        from views.cart_view import CartView
        self.clear_content()
        CartView(self.content_area, self.user, self.controllers, self.update_cart_count).pack(fill=tk.BOTH, expand=True)
    
    def load_orders(self):
        from views.orders_view import CustomerOrdersView
        self.clear_content()
        CustomerOrdersView(self.content_area, self.user, self.controllers).pack(fill=tk.BOTH, expand=True)
    
    def load_profile(self):
        from views.profile_view import ProfileView
        self.clear_content()
        ProfileView(self.content_area, self.user, self.controllers).pack(fill=tk.BOTH, expand=True)
