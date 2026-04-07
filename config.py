import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mysqlvivo')
DB_NAME = os.getenv('DB_NAME', 'smartspend')

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'smartspend_super_secret_change_in_production')
JWT_ALGORITHM = 'HS256'

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'flask_dev_secret')
DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
PORT = int(os.getenv('PORT', 5000))
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Application Configuration
APP_NAME = 'SmartSpend'
APP_VERSION = '1.0.0'
