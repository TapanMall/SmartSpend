from flask import Blueprint, request, jsonify, current_app
from utils.auth import token_required
import decimal
import math
from datetime import datetime

investments_bp = Blueprint('investments', __name__)

def get_db():
    return current_app.config['DB']

def _to_float(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    return float(value or 0)

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

def _parse_date_yyyy_mm_dd(value, *, field_name: str = "date"):
    if not value or not isinstance(value, str):
        return None, f"Invalid {field_name} format. Use YYYY-MM-DD"
    try:
        dt = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None, f"Invalid {field_name} format. Use YYYY-MM-DD"
    return dt.strftime("%Y-%m-%d"), None

@investments_bp.route('/', methods=['GET'])
@token_required
def get_investments():
    user_id = request.current_user['user_id']
    db = get_db()
    investments = db.get_investments(user_id)
    
    for inv in investments:
        inv['amount'] = _to_float(inv.get('amount'))
        if inv.get('date'):
            inv['date'] = inv['date'].strftime('%Y-%m-%d')
            
    return jsonify({"investments": investments}), 200

@investments_bp.route('/', methods=['POST'])
@token_required
def create_investment():
    data = request.get_json()
    user_id = request.current_user['user_id']
    db = get_db()
    
    name = data.get('name')
    type = data.get('type', 'Stocks')
    amount = data.get('amount', 0)
    date = data.get('date')
    notes = data.get('notes', '')
    
    if not name or amount is None or not date:
        return jsonify({"error": "Missing required fields (name, amount, date)"}), 400

    amount_val, err = _parse_positive_amount(amount)
    if err:
        return jsonify({"error": err}), 400
    date_val, err = _parse_date_yyyy_mm_dd(date)
    if err:
        return jsonify({"error": err}), 400
        
    try:
        investment = db.create_investment(user_id, name, type, amount_val, date_val, notes)
        if investment:
            investment['amount'] = _to_float(investment['amount'])
            if investment.get('date'):
                investment['date'] = investment['date'].strftime('%Y-%m-%d')
            return jsonify({"message": "Investment created", "investment": investment}), 201
        return jsonify({"error": "Failed to create investment"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@investments_bp.route('/<int:inv_id>', methods=['DELETE'])
@token_required
def delete_investment(inv_id):
    user_id = request.current_user['user_id']
    db = get_db()
    
    try:
        deleted = db.delete_investment(inv_id, user_id)
        if not deleted:
            return jsonify({"error": "Investment not found"}), 404
        return jsonify({"message": "Investment deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
