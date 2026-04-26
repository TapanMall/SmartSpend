from flask import Blueprint, request, jsonify, current_app
from utils.database import Database
from utils.auth import token_required
import decimal
import math

budgets_bp = Blueprint('budgets', __name__)

def get_db():
    return current_app.config['DB']

def _serialize(obj):
    """Convert Decimal to float for JSON serialization."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return obj

def _format_budget(b):
    return {
        'id': b['id'],
        'user_id': b['user_id'],
        'category': b['category'],
        'amount': float(b['amount']),
        'spent': float(b.get('spent', 0)),
        'created_at': str(b.get('created_at', ''))
    }

def _parse_positive_amount(value, *, field_name: str = "amount"):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return None, f"Invalid {field_name} format"
    if not math.isfinite(amount):
        return None, f"Invalid {field_name} value"
    if amount <= 0:
        return None, f"{field_name} must be greater than zero"
    return amount, None

@budgets_bp.route('/', methods=['GET', 'POST'])
@token_required
def budgets():
    try:
        db = get_db()
        user_id = request.current_user['user_id']

        if request.method == 'GET':
            budget_list = db.get_budgets_with_spending(user_id)
            return jsonify({'budgets': [_format_budget(b) for b in budget_list]}), 200

        elif request.method == 'POST':
            data = request.get_json()
            category = data.get('category')
            amount = data.get('amount')

            if not category or amount is None:
                return jsonify({'error': 'Missing required fields'}), 400

            amount_val, err = _parse_positive_amount(amount)
            if err:
                return jsonify({'error': err}), 400

            budget = db.create_budget(user_id, category, amount_val)
            if budget:
                return jsonify({'message': 'Budget created successfully', 'budget': _format_budget(budget)}), 201
            return jsonify({'error': 'Failed to create budget'}), 500

    except Exception as e:
        err_str = str(e)
        current_app.logger.error(err_str)
        # Duplicate budget for same category
        if 'Duplicate entry' in err_str or '1062' in err_str:
            return jsonify({'error': f'A budget for this category already exists. Delete or update it instead.'}), 409
        return jsonify({'error': 'An internal server error occurred'}), 500

@budgets_bp.route('/<int:budget_id>', methods=['PUT', 'DELETE'])
@token_required
def budget_detail(budget_id):
    try:
        db = get_db()
        user_id = request.current_user['user_id']

        if request.method == 'PUT':
            data = request.get_json()
            category = data.get('category')
            amount = data.get('amount')
            if not category or amount is None:
                return jsonify({'error': 'Missing required fields'}), 400

            amount_val, err = _parse_positive_amount(amount)
            if err:
                return jsonify({'error': err}), 400

            budget = db.update_budget(user_id, budget_id, category, amount_val)
            if budget:
                return jsonify({'message': 'Budget updated successfully', 'budget': _format_budget(budget)}), 200
            return jsonify({'error': 'Failed to update budget or budget not found'}), 404

        elif request.method == 'DELETE':
            db.delete_budget(user_id, budget_id)
            return jsonify({'message': 'Budget deleted successfully'}), 200

    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500
