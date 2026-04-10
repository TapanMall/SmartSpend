from flask import Blueprint, jsonify, request, current_app
from utils.database import Database
from utils.auth import token_required

analytics_bp = Blueprint('analytics', __name__)

def get_db():
    return current_app.config['DB']

@analytics_bp.route('/summary', methods=['GET'])
@token_required
def get_summary():
    try:
        from app import cache
        user_id = request.current_user['user_id']
        
        # Use simple cache
        cache_key = f'analytics_summary_{user_id}'
        summary = cache.get(cache_key)
        
        if summary is None:
            db = get_db()
            summary = db.get_analytics_summary(user_id)
            cache.set(cache_key, summary, timeout=300) # 5 minutes TTL
            
        return jsonify(summary)
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500
