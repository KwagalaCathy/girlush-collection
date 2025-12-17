"""
Helper utilities for Girlush Collections
"""
from datetime import datetime
import re

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"UGX {amount:,.0f}"

def format_date(date_string: str) -> str:
    """Format ISO date string to readable format"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%B %d, %Y %I:%M %p")
    except:
        return date_string

def format_date_short(date_string: str) -> str:
    """Format ISO date string to short format"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%m/%d/%Y")
    except:
        return date_string

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number (Philippine format)"""
    # Allow various formats: 09XXXXXXXXX, +639XXXXXXXXX, 9XXXXXXXXX
    pattern = r'^(\+?63|0)?9\d{9}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def calculate_profit(cost: float, price: float, quantity: int) -> float:
    """Calculate profit for product sale"""
    return (price - cost) * quantity

def get_status_color(status: str) -> str:
    """Get color for order status"""
    status_colors = {
        'pending': '#FFC107',  # Warning
        'processing': '#17A2B8',  # Info
        'completed': '#28A745',  # Success
        'cancelled': '#DC3545'  # Danger
    }
    return status_colors.get(status.lower(), '#6C757D')

def paginate_list(items: list, page: int, items_per_page: int) -> tuple:
    """
    Paginate a list
    Returns: (paginated_items, total_pages, start_index, end_index)
    """
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, total_items)
    
    paginated_items = items[start_index:end_index]
    
    return paginated_items, total_pages, start_index, end_index
