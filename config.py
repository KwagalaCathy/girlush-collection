"""
Configuration settings for Girlush Collections Inventory Management System
"""
import os

# Application Settings
APP_NAME = "Girlush Collections"
APP_VERSION = "1.0.0"
WINDOW_TITLE = f"{APP_NAME} - Inventory Management"

# Database Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "girlush_inventory.db")

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 1000
MIN_WINDOW_HEIGHT = 600

# Color Scheme
PRIMARY_COLOR = "#FF1493"  # Deep Pink
SECONDARY_COLOR = "#FFB6C1"  # Light Pink
ACCENT_COLOR = "#FF69B4"  # Hot Pink
BG_COLOR = "#F8F9FA"
TEXT_COLOR = "#212529"
SUCCESS_COLOR = "#28A745"
WARNING_COLOR = "#FFC107"
DANGER_COLOR = "#DC3545"
INFO_COLOR = "#17A2B8"

# Font Settings
FONT_FAMILY = "Segoe UI"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 10
FONT_SIZE_MEDIUM = 12
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 16
FONT_SIZE_TITLE = 20

# Pagination
ITEMS_PER_PAGE = 20

# Business Settings
LOW_STOCK_THRESHOLD = 10
TAX_RATE = 0.0  # 0% tax

# Default Admin Credentials
DEFAULT_ADMIN_EMAIL = "xandercaitlyn0@gmail.com"
DEFAULT_ADMIN_PASSWORD = "cathie"
DEFAULT_ADMIN_NAME = "Admin"

# Logging
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
