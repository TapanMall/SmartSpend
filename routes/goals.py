from flask import Blueprint, request, jsonify, current_app
from utils.database import Database
from utils.auth import token_required
import decimal

goals_bp = Blueprint('goals', __name__)

def get_db():
    return current_app.config['DB']

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
        db = get_db()
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
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500


@goals_bp.route('/<int:goal_id>/add', methods=['POST'])
@token_required
def add_goal_funds(goal_id):
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        data = request.get_json()
        amount_to_add = float(data.get('amount', 0))

        if amount_to_add <= 0:
            return jsonify({'error': 'Amount must be greater than zero'}), 400

        # Verify goal belongs to user
        goal = db.fetch_one("SELECT * FROM goals WHERE id = %s AND user_id = %s", (goal_id, user_id))
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404

        new_total = float(goal.get('current_amount') or 0) + amount_to_add
        db.execute("UPDATE goals SET current_amount = %s WHERE id = %s", (new_total, goal_id))
        
        return jsonify({'message': 'Goal progress updated successfully', 'new_total': new_total}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500
