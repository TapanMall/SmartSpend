"""
utils/jwt_helper.py — Token creation, decoding, and @require_auth decorator
"""
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, g
from config import JWT_SECRET, JWT_ALGO, JWT_EXPIRY_HOURS, JWT_REFRESH_DAYS

def create_access_token(user_id: int, email: str) -> str:
    payload = {
        'sub': str(user_id),
        'email': email,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS),
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def create_refresh_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=JWT_REFRESH_DAYS),
        'type': 'refresh'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token: str) -> dict:
    """Decode and verify. Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError."""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])

def _extract_token() -> str | None:
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        return auth[7:]
    # Also accept token in cookie for browser use
    return request.cookies.get('access_token')

def require_auth(f):
    """Decorator: validates JWT and sets g.user_id + g.email."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_token()
        if not token:
            return jsonify({'error': 'Authentication required', 'code': 'NO_TOKEN'}), 401
        try:
            payload = decode_token(token)
            if payload.get('type') != 'access':
                raise jwt.InvalidTokenError('Wrong token type')
            g.user_id = payload['sub']
            g.email   = payload['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired', 'code': 'TOKEN_EXPIRED'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': 'Invalid token', 'code': 'INVALID_TOKEN'}), 401
        return f(*args, **kwargs)
    return decorated
