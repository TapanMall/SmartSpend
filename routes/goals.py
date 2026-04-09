from flask import Blueprint, request, jsonify
from utils.database import Database
from utils.auth import token_required
import decimal

goals_bp = Blueprint('goals', __name__)
db = Database()

def _format_goal(g):
    return {
        'id': g['id'],
        'user_id': g['user_id'],
        'name': g['name'],
        'target_amount': float(g['target_amount']),
        'current_amount': float(g.get('current_amount') or 0),
        'created_at': str(g.get('created_at', ''))
    }

@goals_bp.route('/', methods=['GET', 'POST'])
@token_required
def goals():
    try:
        user_id = request.current_user['user_id']

        if request.method == 'GET':
            goal_list = db.get_goals(user_id)
            return jsonify({'goals': [_format_goal(g) for g in goal_list]}), 200

        elif request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            target_amount = data.get('target_amount')
            current_amount = data.get('current_amount', 0)

            if not name or target_amount is None:
                return jsonify({'error': 'Missing required fields'}), 400

            goal = db.create_goal(user_id, name, float(target_amount), float(current_amount))
            if goal:
                return jsonify({'message': 'Goal created successfully', 'goal': _format_goal(goal)}), 201
            return jsonify({'error': 'Failed to create goal'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
