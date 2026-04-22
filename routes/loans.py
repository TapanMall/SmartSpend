from flask import Blueprint, request, jsonify, current_app
from utils.auth import token_required
import decimal

loans_bp = Blueprint('loans', __name__)

def get_db():
    return current_app.config['DB']

def _to_float(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    return float(value or 0)

@loans_bp.route('/', methods=['GET'])
@token_required
def get_loans():
    user_id = request.current_user['user_id']
    db = get_db()
    query = "SELECT * FROM loans WHERE user_id = %s ORDER BY created_at DESC"
    loans = db.fetch_all(query, (user_id,))
    
    # Format decimal values
    for loan in loans:
        loan['total_amount'] = _to_float(loan.get('total_amount'))
        loan['emi_amount'] = _to_float(loan.get('emi_amount'))
        loan['outstanding_amount'] = _to_float(loan.get('outstanding_amount'))
        loan['interest_rate'] = _to_float(loan.get('interest_rate'))
        
    return jsonify({"loans": loans}), 200

@loans_bp.route('/', methods=['POST'])
@token_required
def create_loan():
    data = request.get_json()
    user_id = request.current_user['user_id']
    db = get_db()
    name = data.get('name')
    type = data.get('type', 'Personal')
    total_amount = data.get('total_amount', 0)
    emi_amount = data.get('emi_amount', 0)
    outstanding_amount = data.get('outstanding_amount', 0)
    interest_rate = data.get('interest_rate', 0)
    
    if not name or not total_amount:
        return jsonify({"error": "Missing name or total amount"}), 400
        
    query = """
        INSERT INTO loans (user_id, name, type, total_amount, emi_amount, outstanding_amount, interest_rate, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    try:
        loan_id = db.execute(query, (user_id, name, type, total_amount, emi_amount, outstanding_amount, interest_rate))
        
        loan = db.fetch_one("SELECT * FROM loans WHERE id = %s", (loan_id,))
        if loan:
            loan['total_amount'] = float(loan['total_amount'])
            loan['emi_amount'] = float(loan['emi_amount'])
            loan['outstanding_amount'] = float(loan['outstanding_amount'])
            loan['interest_rate'] = float(loan['interest_rate'])
            return jsonify({"message": "Loan created", "loan": loan}), 201
        return jsonify({"error": "Failed to create loan"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@loans_bp.route('/<int:loan_id>', methods=['PUT'])
@token_required
def update_loan(loan_id):
    data = request.get_json()
    user_id = request.current_user['user_id']
    db = get_db()
    
    name = data.get('name')
    type = data.get('type')
    total_amount = data.get('total_amount')
    emi_amount = data.get('emi_amount')
    outstanding_amount = data.get('outstanding_amount')
    interest_rate = data.get('interest_rate')
    
    update_fields = []
    params = []
    
    if name is not None:
        update_fields.append("name = %s")
        params.append(name)
    if type is not None:
        update_fields.append("type = %s")
        params.append(type)
    if total_amount is not None:
        update_fields.append("total_amount = %s")
        params.append(total_amount)
    if emi_amount is not None:
        update_fields.append("emi_amount = %s")
        params.append(emi_amount)
    if outstanding_amount is not None:
        update_fields.append("outstanding_amount = %s")
        params.append(outstanding_amount)
    if interest_rate is not None:
        update_fields.append("interest_rate = %s")
        params.append(interest_rate)
        
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400
        
    params.extend([loan_id, user_id])
    query = f"UPDATE loans SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
    
    try:
        db.execute(query, tuple(params))
        return jsonify({"message": "Loan updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@loans_bp.route('/<int:loan_id>', methods=['DELETE'])
@token_required
def delete_loan(loan_id):
    user_id = request.current_user['user_id']
    db = get_db()
    query = "DELETE FROM loans WHERE id = %s AND user_id = %s"
    
    try:
        db.execute(query, (loan_id, user_id))
        return jsonify({"message": "Loan deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
