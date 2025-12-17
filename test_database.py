"""
Test database and login functionality
"""
from database.database_manager import DatabaseManager
from controllers.auth_controller import AuthController

print("="*60)
print("DATABASE & LOGIN TEST")
print("="*60)

# Initialize
db = DatabaseManager()
auth = AuthController(db)

# Test 1: Admin Login
print("\n1. Testing Admin Login...")
success, user, msg = auth.login('xandercaitlyn0@gmail.com', 'cathie')
if success:
    print(f"   ✓ {msg}")
    print(f"   User: {user.name}")
    print(f"   Email: {user.email}")
    print(f"   Role: {user.role}")
else:
    print(f"   ✗ {msg}")

# Test 2: Wrong Password
print("\n2. Testing Wrong Password...")
success, user, msg = auth.login('xandercaitlyn0@gmail.com', 'wrongpassword')
if not success:
    print(f"   ✓ Correctly rejected: {msg}")
else:
    print(f"   ✗ Should have failed")

# Test 3: Non-existent User
print("\n3. Testing Non-existent User...")
success, user, msg = auth.login('nonexistent@test.com', 'password')
if not success:
    print(f"   ✓ Correctly rejected: {msg}")
else:
    print(f"   ✗ Should have failed")

# Test 4: Database Stats
print("\n4. Database Statistics:")
stats = db.get_dashboard_stats()
print(f"   Total Products: {stats['total_products']}")
print(f"   Total Customers: {stats['total_customers']}")
print(f"   Total Orders: {stats['total_orders']}")
print(f"   Total Sales: ₱{stats['total_sales']:,.2f}")

# Test 5: Test Signup
print("\n5. Testing Signup...")
success, msg = auth.register(
    email='testuser@example.com',
    password='password123',
    name='Test User',
    phone='09171234567',
    address='123 Test St',
    city='Test City'
)
if success:
    print(f"   ✓ {msg}")
    # Try login with new user
    success2, user2, msg2 = auth.login('testuser@example.com', 'password123')
    if success2:
        print(f"   ✓ New user can login: {user2.name}")
    else:
        print(f"   ✗ New user login failed: {msg2}")
else:
    print(f"   Note: {msg} (may already exist from previous test)")

print("\n" + "="*60)
print("ALL TESTS COMPLETED!")
print("="*60)
