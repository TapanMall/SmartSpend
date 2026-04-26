from flask import Blueprint, request, jsonify, current_app, make_response
from utils.database import Database
from utils.auth import generate_token, generate_refresh_token, decode_token, token_required
from models.user import User
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from config import GOOGLE_CLIENT_ID
import secrets

auth_bp = Blueprint('auth', __name__)

def get_db():
    return current_app.config['DB']

@auth_bp.route('/google', methods=['POST'])
def google_auth():
    try:
        db = get_db()
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
            refresh_token = generate_refresh_token(User.format_user_data(user))
            resp = make_response(jsonify({
                'access_token': jwt_token,
                'user': User.format_user_data(user)
            }))
            resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=request.is_secure, samesite='Lax', max_age=30*24*60*60)
            return resp
            
        except ValueError as e:
            return jsonify({'error': f'Invalid Google token: {str(e)}'}), 401
            
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@auth_bp.route('/profile-photo', methods=['POST'])
@token_required
def upload_profile_photo():
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        photo_data = data.get('profile_photo')
        if not photo_data:
            return jsonify({'error': 'No photo data provided'}), 400
            
        db.execute("UPDATE users SET profile_photo = %s WHERE id = %s", (photo_data, user_id))
        
        updated_user = db.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
        return jsonify({
            'message': 'Profile photo updated successfully',
            'user': User.format_user_data(updated_user)
        }), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'Failed to upload profile photo'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        db = get_db()
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
            refresh_token = generate_refresh_token(User.format_user_data(user))
            resp = make_response(jsonify({
                'message': 'User registered successfully',
                'access_token': token,
                'user': User.format_user_data(user)
            }), 201)
            resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=request.is_secure, samesite='Lax', max_age=30*24*60*60)
            return resp
        else:
            return jsonify({'error': 'Failed to create user'}), 500
            
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    from app import limiter
    
    @limiter.limit("5 per minute")
    def _login():
        try:
            db = get_db()
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'error': 'Email and password are required'}), 400
                
            user = db.get_user_by_email(email)
            if user and User.verify_password(password, user['password_hash']):
                token = generate_token(User.format_user_data(user))
                refresh_token = generate_refresh_token(User.format_user_data(user))
                resp = make_response(jsonify({
                    'access_token': token,
                    'user': User.format_user_data(user)
                }))
                resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=request.is_secure, samesite='Lax', max_age=30*24*60*60)
                return resp
            else:
                return jsonify({'error': 'Invalid email or password'}), 401
                
        except Exception as e:
            current_app.logger.error(str(e))
            return jsonify({'error': 'An internal server error occurred'}), 500
            
    return _login()

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    try:
        db = get_db()
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            return jsonify({'error': 'Refresh token missing'}), 401
            
        payload = decode_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return jsonify({'error': 'Invalid refresh token'}), 401
            
        user = db.fetch_one("SELECT * FROM users WHERE id = %s", (payload['user_id'],))
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        token = generate_token(User.format_user_data(user))
        new_refresh_token = generate_refresh_token(User.format_user_data(user))
        resp = make_response(jsonify({'access_token': token}))
        resp.set_cookie('refresh_token', new_refresh_token, httponly=True, secure=request.is_secure, samesite='Lax', max_age=30*24*60*60)
        return resp
        
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        full_name = data.get('full_name')
        email = data.get('email')
        phone = data.get('phone', '')
        currency = data.get('currency', '₹ INR — Indian Rupee')
        
        if not full_name or not email:
            return jsonify({'error': 'Full name and email are required'}), 400
            
        if db.update_user_profile(user_id, full_name, email, phone, currency):
            # Fetch updated user to return to frontend
            updated_user = db.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
            if updated_user:
                 return jsonify({
                     'message': 'Profile updated successfully',
                     'user': User.format_user_data(updated_user)
                 }), 200
        return jsonify({'error': 'Failed to update profile'}), 500
        
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@auth_bp.route('/security', methods=['PUT'])
@token_required
def update_security():
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new passwords are required'}), 400
            
        user = db.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
        if not user or not User.verify_password(current_password, user['password_hash']):
            return jsonify({'error': 'Incorrect current password'}), 401
            
        new_password_hash = User.hash_password(new_password)
        if db.update_user_password(user_id, new_password_hash):
            return jsonify({'message': 'Password updated successfully'}), 200
            
        return jsonify({'error': 'Failed to update password'}), 500
        
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@auth_bp.route('/account', methods=['DELETE'])
@token_required
def delete_account():
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        
        if db.delete_user_account(user_id):
            return jsonify({'message': 'Account deleted successfully'}), 200
            
        return jsonify({'error': 'Failed to delete account'}), 500
        
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500
