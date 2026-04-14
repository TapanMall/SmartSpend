import jwt
from datetime import datetime, timedelta, UTC
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.exceptions import HTTPException
from config import JWT_SECRET, JWT_ALGORITHM

def generate_token(user_data):
    """Generate short-lived JWT token for user (15m)"""
    now_utc = datetime.now(UTC)
    payload = {
        'user_id': user_data['id'],
        'email': user_data['email'],
        'full_name': user_data['full_name'],
        'plan': user_data['plan'],
        'exp': now_utc + timedelta(minutes=15),
        'iat': now_utc
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_refresh_token(user_data):
    """Generate long-lived refresh token for user (30d)"""
    now_utc = datetime.now(UTC)
    payload = {
        'user_id': user_data['id'],
        'type': 'refresh',
        'exp': now_utc + timedelta(days=30),
        'iat': now_utc
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check token in header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Bearer token malformed'}), 401
        
        # Check token in localStorage (for web)
        if not token:
            token = request.headers.get('X-Access-Token') or request.cookies.get('token')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            current_user = decode_token(token)
            if not current_user:
                return jsonify({'error': 'Token is invalid'}), 401

            # Add user to request context
            request.current_user = current_user
        except Exception as e:
            # Preserve framework-raised HTTP errors (e.g. 429 from rate limiter).
            if isinstance(e, HTTPException):
                raise
            return jsonify({'error': 'Token is invalid'}), 401

        # Execute wrapped endpoint outside token decode try/except.
        return f(*args, **kwargs)
    
    return decorated
