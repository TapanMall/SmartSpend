from flask import Blueprint, jsonify, request
from utils.database import Database
from utils.auth import token_required

analytics_bp = Blueprint('analytics', __name__)
db = Database()

@analytics_bp.route('/summary', methods=['GET'])
@token_required
def get_summary():
    try:
        user_id = request.current_user['user_id']
        summary = db.get_analytics_summary(user_id)
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
