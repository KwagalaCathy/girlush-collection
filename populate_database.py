"""
Populate the database with sample data for demonstration
"""
from database.database_manager import DatabaseManager
from database.models import Product, Supplier
from controllers.product_controller import ProductController

# Initialize database
db = DatabaseManager()
product_controller = ProductController(db)

# Sample suppliers
suppliers_data = [
    {"name": "Premium Bags Co.", "contact_person": "Maria Santos", "email": "maria@premiumbags.com", "phone": "09171234567", "address": "Makati City"},
    {"name": "Fashion Wholesale", "contact_person": "John Reyes", "email": "john@fashionwholesale.com", "phone": "09281234567", "address": "Quezon City"},
]

print("Adding suppliers...")
supplier_ids = []
for supplier_data in suppliers_data:
    supplier = Supplier(
        name=supplier_data["name"],
        contact_person=supplier_data["contact_person"],
        email=supplier_data["email"],
        phone=supplier_data["phone"],
        address=supplier_data["address"]
    )
    supplier_id = db.create_supplier(supplier)
    if supplier_id:
        supplier_ids.append(supplier_id)
        print(f"✓ Added supplier: {supplier_data['name']}")

# Sample products
products_data = [
    {"name": "Classic Leather Tote", "description": "Elegant leather tote bag perfect for work or casual outings", "category": "Tote Bags", "price": 2500.00, "cost": 1500.00, "stock": 25},
    {"name": "Mini Crossbody Bag", "description": "Compact and stylish crossbody bag for everyday use", "category": "Crossbody Bags", "price": 1800.00, "cost": 1000.00, "stock": 30},
    {"name": "Designer Evening Clutch", "description": "Luxurious evening clutch with crystal embellishments", "category": "Clutches", "price": 3500.00, "cost": 2000.00, "stock": 15},
    {"name": "Canvas Shoulder Bag", "description": "Durable canvas shoulder bag with multiple compartments", "category": "Shoulder Bags", "price": 1500.00, "cost": 800.00, "stock": 40},
    {"name": "Leather Backpack", "description": "Stylish leather backpack with laptop compartment", "category": "Backpacks", "price": 3200.00, "cost": 1800.00, "stock": 20},
    {"name": "Hobo Bag", "description": "Trendy hobo-style bag with soft leather finish", "category": "Hobo Bags", "price": 2200.00, "cost": 1300.00, "stock": 18},
    {"name": "Satchel Bag", "description": "Classic satchel with adjustable strap", "category": "Satchels", "price": 2800.00, "cost": 1600.00, "stock": 22},
    {"name": "Woven Straw Bag", "description": "Summer essential woven straw beach bag", "category": "Beach Bags", "price": 1200.00, "cost": 600.00, "stock": 35},
    {"name": "Quilted Chain Bag", "description": "Elegant quilted bag with gold chain strap", "category": "Chain Bags", "price": 4000.00, "cost": 2500.00, "stock": 12},
    {"name": "Bucket Bag", "description": "Modern bucket bag with drawstring closure", "category": "Bucket Bags", "price": 1900.00, "cost": 1100.00, "stock": 28},
    {"name": "Vintage Messenger Bag", "description": "Retro-style messenger bag for casual wear", "category": "Messenger Bags", "price": 2100.00, "cost": 1200.00, "stock": 20},
    {"name": "Metallic Clutch", "description": "Shimmering metallic clutch for special occasions", "category": "Clutches", "price": 2800.00, "cost": 1500.00, "stock": 10},
    {"name": "Convertible Backpack Tote", "description": "Versatile bag that converts from backpack to tote", "category": "Convertible Bags", "price": 3500.00, "cost": 2000.00, "stock": 15},
    {"name": "Faux Fur Crossbody", "description": "Trendy faux fur crossbody bag", "category": "Crossbody Bags", "price": 2400.00, "cost": 1400.00, "stock": 8},
    {"name": "Travel Weekender Bag", "description": "Spacious weekender bag perfect for short trips", "category": "Travel Bags", "price": 4500.00, "cost": 2800.00, "stock": 12},
]

print("\nAdding products...")
for i, product_data in enumerate(products_data):
    supplier_id = supplier_ids[i % len(supplier_ids)] if supplier_ids else None
    
    success, message = product_controller.create_product(
        name=product_data["name"],
        description=product_data["description"],
        category=product_data["category"],
        price=product_data["price"],
        cost=product_data["cost"],
        stock_quantity=product_data["stock"],
        supplier_id=supplier_id
    )
    
    if success:
        print(f"✓ Added: {product_data['name']} - Stock: {product_data['stock']} - Price: ₱{product_data['price']:,.2f}")
    else:
        print(f"✗ Failed to add: {product_data['name']}")

print(f"\n{'='*60}")
print("DATABASE POPULATION COMPLETE!")
print(f"{'='*60}")
print(f"\n✓ Database location: {db.db_path}")
print(f"✓ Total suppliers added: {len(supplier_ids)}")
print(f"✓ Total products added: {len(products_data)}")
print(f"\n📊 To view in DB Browser for SQLite:")
print(f"   1. Open DB Browser for SQLite")
print(f"   2. Click 'Open Database'")
print(f"   3. Browse to: {db.db_path}")
print(f"\n🔐 Default Admin Login:")
print(f"   Email: xandercaitlyn0@gmail.com")
print(f"   Password: cathie")
print(f"\n{'='*60}")

# Display statistics
stats = db.get_dashboard_stats()
print(f"\n📈 CURRENT DATABASE STATISTICS:")
print(f"   • Total Products: {stats['total_products']}")
print(f"   • Total Customers: {stats['total_customers']}")
print(f"   • Total Orders: {stats['total_orders']}")
print(f"   • Low Stock Products: {stats['low_stock_products']}")
print(f"{'='*60}\n")
