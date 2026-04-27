from flask import Blueprint, request, jsonify, current_app
from utils.auth import token_required
import decimal
import math

loans_bp = Blueprint('loans', __name__)

def get_db():
    return current_app.config['DB']

def _to_float(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    return float(value or 0)

def _parse_number(value, *, field_name: str):
    try:
        n = float(value)
    except (TypeError, ValueError):
        return None, f"Invalid {field_name} format"
    if not math.isfinite(n):
        return None, f"Invalid {field_name} value"
    return n, None

def _parse_non_negative(value, *, field_name: str):
    n, err = _parse_number(value, field_name=field_name)
    if err:
        return None, err
    if n < 0:
        return None, f"{field_name} must be non-negative"
    return n, None

def _parse_positive(value, *, field_name: str):
    n, err = _parse_non_negative(value, field_name=field_name)
    if err:
        return None, err
    if n <= 0:
        return None, f"{field_name} must be greater than zero"
    return n, None

@loans_bp.route('/', methods=['GET'])
@token_required
def get_loans():
    user_id = request.current_user['user_id']
    db = get_db()
    query = "SELECT * FROM loans WHERE user_id = %s ORDER BY created_at DESC"
    loans = db.fetch_all(query, (user_id,))
    
    # Format decimal values and fetch emi history
    for loan in loans:
        loan['total_amount'] = _to_float(loan.get('total_amount'))
        loan['emi_amount'] = _to_float(loan.get('emi_amount'))
        loan['outstanding_amount'] = _to_float(loan.get('outstanding_amount'))
        loan['interest_rate'] = _to_float(loan.get('interest_rate'))
        
        # Format dates to string
        if loan.get('start_date'):
            loan['start_date'] = loan['start_date'].strftime('%Y-%m-%d')
        if loan.get('end_date'):
            loan['end_date'] = loan['end_date'].strftime('%Y-%m-%d')
            
        emi_query = "SELECT * FROM emi_history WHERE loan_id = %s ORDER BY payment_date DESC"
        emis = db.fetch_all(emi_query, (loan['id'],))
        for emi in emis:
            emi['amount_paid'] = _to_float(emi.get('amount_paid'))
            emi['principal_paid'] = _to_float(emi.get('principal_paid'))
            emi['interest_paid'] = _to_float(emi.get('interest_paid'))
            if emi.get('payment_date'):
                emi['payment_date'] = emi['payment_date'].strftime('%Y-%m-%d')
        loan['emi_history'] = emis
        
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
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    tenure_months = data.get('tenure_months', 0)
    
    if not name or total_amount is None:
        return jsonify({"error": "Missing name or total amount"}), 400

    total_val, err = _parse_positive(total_amount, field_name="total_amount")
    if err:
        return jsonify({"error": err}), 400
    emi_val, err = _parse_non_negative(emi_amount, field_name="emi_amount")
    if err:
        return jsonify({"error": err}), 400
    outstanding_val, err = _parse_non_negative(outstanding_amount, field_name="outstanding_amount")
    if err:
        return jsonify({"error": err}), 400
    if outstanding_val > total_val:
        return jsonify({"error": "outstanding_amount cannot exceed total_amount"}), 400
    rate_val, err = _parse_non_negative(interest_rate, field_name="interest_rate")
    if err:
        return jsonify({"error": err}), 400
    if rate_val > 100:
        return jsonify({"error": "interest_rate is unrealistically high"}), 400
        
    query = """
        INSERT INTO loans (user_id, name, type, total_amount, emi_amount, outstanding_amount, interest_rate, start_date, end_date, tenure_months, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    try:
        loan_id = db.execute(query, (user_id, name, type, total_val, emi_val, outstanding_val, rate_val, start_date, end_date, tenure_months))
        
        loan = db.fetch_one("SELECT * FROM loans WHERE id = %s", (loan_id,))
        if loan:
            loan['total_amount'] = _to_float(loan['total_amount'])
            loan['emi_amount'] = _to_float(loan['emi_amount'])
            loan['outstanding_amount'] = _to_float(loan['outstanding_amount'])
            loan['interest_rate'] = _to_float(loan['interest_rate'])
            if loan.get('start_date'):
                loan['start_date'] = loan['start_date'].strftime('%Y-%m-%d')
            if loan.get('end_date'):
                loan['end_date'] = loan['end_date'].strftime('%Y-%m-%d')
            loan['emi_history'] = []
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

@loans_bp.route('/<int:loan_id>/pay', methods=['POST'])
@token_required
def pay_emi(loan_id):
    data = request.get_json()
    user_id = request.current_user['user_id']
    db = get_db()
    
    # Verify loan belongs to user
    loan = db.fetch_one("SELECT * FROM loans WHERE id = %s AND user_id = %s", (loan_id, user_id))
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
        
    amount_paid_raw = data.get('amount_paid', loan.get('emi_amount', 0))
    amount_paid, err = _parse_positive(amount_paid_raw, field_name="amount_paid")
    if err:
        return jsonify({"error": err}), 400
    
    # Calculate interest portion
    annual_rate = _to_float(loan.get('interest_rate', 0))
    if annual_rate < 0:
        return jsonify({"error": "Invalid interest rate"}), 400
    monthly_rate = annual_rate / 12 / 100
    interest_paid = _to_float(loan.get('outstanding_amount', 0)) * monthly_rate
    principal_paid = amount_paid - interest_paid
    if principal_paid < 0:
        principal_paid = 0
        
    # Update outstanding amount
    new_outstanding = max(0, _to_float(loan.get('outstanding_amount', 0)) - principal_paid)
    
    try:
        # Update loan
        db.execute("UPDATE loans SET outstanding_amount = %s WHERE id = %s", (new_outstanding, loan_id))
        
        # Insert EMI history
        db.execute("""
            INSERT INTO emi_history (loan_id, amount_paid, principal_paid, interest_paid, payment_date, status)
            VALUES (%s, %s, %s, %s, NOW(), 'PAID')
        """, (loan_id, amount_paid, principal_paid, interest_paid))
        
        return jsonify({"message": "EMI payment successful", "new_outstanding": new_outstanding}), 200
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
