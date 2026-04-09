from flask import Blueprint, request, jsonify
from utils.database import Database
from utils.auth import generate_token
from models.user import User
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from config import GOOGLE_CLIENT_ID
import secrets

auth_bp = Blueprint('auth', __name__)
db = Database()

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    try:
        data = request.get_json()
        token = data.get('credential')
        
        if not token:
            return jsonify({'error': 'Missing Google credential'}), 400
            
        try:
            # For development without a real client ID, we might skip verification
            # But here we implement the real logic
            if GOOGLE_CLIENT_ID == 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com':
                # Mock decode for demo purposes if client ID is not set
                import jwt
                idinfo = jwt.decode(token, options={"verify_signature": False})
            else:
                idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
                
            email = idinfo.get('email')
            full_name = idinfo.get('name', 'Google User')
            
            if not email:
                return jsonify({'error': 'Google token did not contain an email'}), 400
                
            user = db.get_user_by_email(email)
            if not user:
                # Sign Up Flow
                random_pass = secrets.token_urlsafe(16)
                password_hash = User.hash_password(random_pass)
                if db.create_user(email, password_hash, full_name):
                    user = db.get_user_by_email(email)
                else:
                    return jsonify({'error': 'Failed to create user from Google account'}), 500
                    
            # Sign In Flow (also runs after Sign Up)
            jwt_token = generate_token(User.format_user_data(user))
            return jsonify({
                'access_token': jwt_token,
                'user': User.format_user_data(user)
            })
            
        except ValueError as e:
            return jsonify({'error': f'Invalid Google token: {str(e)}'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
            
        # Check if user already exists
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
            
        # Create user
        password_hash = User.hash_password(password)
        if db.create_user(email, password_hash, full_name):
            user = db.get_user_by_email(email)
            token = generate_token(User.format_user_data(user))
            return jsonify({
                'message': 'User registered successfully',
                'access_token': token,
                'user': User.format_user_data(user)
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
            
        user = db.get_user_by_email(email)
        if user and User.verify_password(password, user['password_hash']):
            token = generate_token(User.format_user_data(user))
            return jsonify({
                'access_token': token,
                'user': User.format_user_data(user)
            })
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from utils.auth import token_required

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        full_name = data.get('full_name')
        email = data.get('email')
        
        if not full_name or not email:
            return jsonify({'error': 'Full name and email are required'}), 400
            
        if db.update_user_profile(user_id, full_name, email):
            # Fetch updated user to return to frontend
            updated_user = db.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
            if updated_user:
                 return jsonify({
                     'message': 'Profile updated successfully',
                     'user': User.format_user_data(updated_user)
                 }), 200
        return jsonify({'error': 'Failed to update profile'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

