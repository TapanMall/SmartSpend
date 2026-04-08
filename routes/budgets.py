from flask import Blueprint, request, jsonify
from utils.database import Database
from utils.auth import token_required
import decimal

budgets_bp = Blueprint('budgets', __name__)
db = Database()

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
        'created_at': str(b.get('created_at', ''))
    }

@budgets_bp.route('/', methods=['GET', 'POST'])
@token_required
def budgets():
    try:
        user_id = request.current_user['user_id']

        if request.method == 'GET':
            budget_list = db.get_budgets(user_id)
            return jsonify({'budgets': [_format_budget(b) for b in budget_list]}), 200

        elif request.method == 'POST':
            data = request.get_json()
            category = data.get('category')
            amount = data.get('amount')

            if not category or amount is None:
                return jsonify({'error': 'Missing required fields'}), 400

            budget = db.create_budget(user_id, category, float(amount))
            if budget:
                return jsonify({'message': 'Budget created successfully', 'budget': _format_budget(budget)}), 201
            return jsonify({'error': 'Failed to create budget'}), 500

    except Exception as e:
        err_str = str(e)
        # Duplicate budget for same category
        if 'Duplicate entry' in err_str or '1062' in err_str:
            return jsonify({'error': f'A budget for this category already exists. Delete or update it instead.'}), 409
        return jsonify({'error': err_str}), 500
