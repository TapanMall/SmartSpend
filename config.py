import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', '')

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', '')
JWT_ALGORITHM = 'HS256'

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'flask_dev_secret')
DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
PORT = int(os.getenv('PORT', 5000))
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://yourdomain.com')

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')

# Application Configuration
APP_NAME = 'SmartSpend'
APP_VERSION = '1.0.0'

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com')
