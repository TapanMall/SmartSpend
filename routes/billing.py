from flask import Blueprint, request, jsonify, current_app
from utils.auth import token_required
from utils.database import Database

billing_bp = Blueprint('billing', __name__)

def get_db():
    return current_app.config['DB']

@billing_bp.route('/', methods=['GET'])
@token_required
def get_billing_info():
    db = get_db()
    user_id = request.current_user['user_id']
    
    # 1. Fetch or create User Billing Config
    billing = db.fetch_one("SELECT * FROM user_billing WHERE user_id = %s", (user_id,))
    if not billing:
        db.execute("""
            INSERT INTO user_billing (user_id, plan_type, billing_email, address, country, business_tax_id)
            VALUES (%s, 'STARTER', '', '', '', '')
        """, (user_id,))
        billing = db.fetch_one("SELECT * FROM user_billing WHERE user_id = %s", (user_id,))
    
    # 2. Fetch Payment Methods
    payment_methods = db.fetch_all("SELECT * FROM user_payment_methods WHERE user_id = %s", (user_id,))
    
    # 3. Fetch Invoices
    invoices = db.fetch_all("SELECT * FROM user_invoices WHERE user_id = %s ORDER BY date_issued DESC", (user_id,))

    return jsonify({
        'status': 'success',
        'billing': {
            'plan_type': billing['plan_type'],
            'billing_email': billing['billing_email'],
            'address': billing['address'],
            'country': billing['country'],
            'business_tax_id': billing['business_tax_id']
        },
        'payment_methods': payment_methods,
        'invoices': [{'amount': float(i['amount']), 'invoice_number': i['invoice_number'], 'status': i['status'], 'date_issued': str(i['date_issued'])} for i in invoices]
    })

@billing_bp.route('/update_plan', methods=['POST'])
@token_required
def update_plan():
    db = get_db()
    user_id = request.current_user['user_id']
    data = request.get_json()
    new_plan = data.get('plan_type')
    
    if new_plan not in ['STARTER', 'PRO', 'TEAM']:
        return jsonify({'error': 'Invalid plan type'}), 400
        
    db.execute("UPDATE user_billing SET plan_type = %s WHERE user_id = %s", (new_plan, user_id))
    # Also update the plan in users table for consistency if needed, but let's keep it isolated
    db.execute("UPDATE users SET plan = %s WHERE id = %s", (new_plan.lower(), user_id))
    
    return jsonify({'status': 'success', 'message': f'Upgraded to {new_plan} Plan'})

@billing_bp.route('/update_config', methods=['POST'])
@token_required
def update_config():
    db = get_db()
    user_id = request.current_user['user_id']
    data = request.get_json()
    
    email = data.get('billing_email', '')
    address = data.get('address', '')
    country = data.get('country', '')
    tax_id = data.get('business_tax_id', '')
    
    db.execute("""
        UPDATE user_billing 
        SET billing_email = %s, address = %s, country = %s, business_tax_id = %s
        WHERE user_id = %s
    """, (email, address, country, tax_id, user_id))
    
    return jsonify({'status': 'success', 'message': 'Billing information updated'})

@billing_bp.route('/add_card', methods=['POST'])
@token_required
def add_card():
    db = get_db()
    user_id = request.current_user['user_id']
    data = request.get_json()
    last4 = data.get('last4', '4242')
    brand = data.get('brand', 'Visa').capitalize()
    
    # Remove default from old cards
    db.execute("UPDATE user_payment_methods SET is_default = FALSE WHERE user_id = %s", (user_id,))
    
    db.execute("""
        INSERT INTO user_payment_methods (user_id, card_last4, exp_month, exp_year, brand, is_default)
        VALUES (%s, %s, 12, 2028, %s, TRUE)
    """, (user_id, last4, brand))
    
    return jsonify({'status': 'success', 'message': 'Card added successfully'})

# Endpoint to seed some dummy data (payment methods and invoices) for UI verification
@billing_bp.route('/seed', methods=['POST'])
@token_required
def seed_dummy_data():
    db = get_db()
    user_id = request.current_user['user_id']
    
    # Check if empty
    pm = db.fetch_one("SELECT id FROM user_payment_methods WHERE user_id = %s", (user_id,))
    if not pm:
        db.execute("""
            INSERT INTO user_payment_methods (user_id, card_last4, exp_month, exp_year, brand, is_default)
            VALUES (%s, '4242', 12, 2028, 'Visa', TRUE)
        """, (user_id,))
        
    inv = db.fetch_one("SELECT id FROM user_invoices WHERE user_id = %s", (user_id,))
    if not inv:
        db.execute("INSERT INTO user_invoices (user_id, amount, invoice_number, status, date_issued) VALUES (%s, 0.00, 'QJTKKF-00003', 'PAID', '2026-03-28')", (user_id,))
        db.execute("INSERT INTO user_invoices (user_id, amount, invoice_number, status, date_issued) VALUES (%s, 0.00, 'QJTKKF-00002', 'PAID', '2026-02-28')", (user_id,))
        db.execute("INSERT INTO user_invoices (user_id, amount, invoice_number, status, date_issued) VALUES (%s, 0.00, 'QJTKKF-00001', 'PAID', '2026-01-28')", (user_id,))
            
    return jsonify({'status': 'success'})

@billing_bp.route('/cancel', methods=['POST'])
@token_required
def cancel_subscription():
    db = get_db()
    user_id = request.current_user['user_id']
    
    # Update billing record
    db.execute("UPDATE user_billing SET plan_type = 'STARTER' WHERE user_id = %s", (user_id,))
    # Core user setting
    db.execute("UPDATE users SET plan = 'free' WHERE id = %s", (user_id,))
    
    return jsonify({'status': 'success', 'message': 'Subscription canceled.'})

