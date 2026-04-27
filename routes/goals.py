from flask import Blueprint, request, jsonify, current_app
from utils.database import Database
from utils.auth import token_required
import decimal
import math

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

def _parse_non_negative_amount(value, *, field_name: str):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return None, f"Invalid {field_name} format"
    if not math.isfinite(amount):
        return None, f"Invalid {field_name} value"
    if amount < 0:
        return None, f"{field_name} must be non-negative"
    return amount, None

def _parse_positive_amount(value, *, field_name: str):
    amount, err = _parse_non_negative_amount(value, field_name=field_name)
    if err:
        return None, err
    if amount <= 0:
        return None, f"{field_name} must be greater than zero"
    return amount, None

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

            target_val, err = _parse_positive_amount(target_amount, field_name="target_amount")
            if err:
                return jsonify({'error': err}), 400
            current_val, err = _parse_non_negative_amount(current_amount, field_name="current_amount")
            if err:
                return jsonify({'error': err}), 400

            goal = db.create_goal(user_id, name, target_val, current_val)
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

@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@token_required
def delete_goal_route(goal_id):
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        db.delete_goal(user_id, goal_id)
        return jsonify({'message': 'Goal deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500
