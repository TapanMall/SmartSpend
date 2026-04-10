from flask import Blueprint, request, jsonify, Response, current_app
from utils.auth import token_required
from utils.database import Database
import csv
import io
import json

reports_bp = Blueprint('reports', __name__)

def get_db():
    return current_app.config['DB']

@reports_bp.route('/export_json', methods=['GET'])
@token_required
def export_json():
    db = get_db()
    user_id = request.current_user['user_id']
    
    user = db.fetch_one("SELECT id, email, full_name, plan, created_at, phone, currency FROM users WHERE id = %s", (user_id,))
    if user and user.get('created_at'):
        user['created_at'] = str(user['created_at'])

    transactions = db.get_transactions(user_id, limit=10000)
    for t in transactions:
        if 'date' in t and t['date'] is not None: t['date'] = str(t['date'])
        if 'created_at' in t and t['created_at'] is not None: t['created_at'] = str(t['created_at'])
        if 'amount' in t and t['amount'] is not None: t['amount'] = float(t['amount'])
        
    budgets = db.get_budgets(user_id)
    for b in budgets:
        if 'created_at' in b and b['created_at'] is not None: b['created_at'] = str(b['created_at'])
        if 'amount' in b and b['amount'] is not None: b['amount'] = float(b['amount'])

    goals = db.get_goals(user_id)
    for g in goals:
        if 'created_at' in g and g['created_at'] is not None: g['created_at'] = str(g['created_at'])
        if 'target_amount' in g and g['target_amount'] is not None: g['target_amount'] = float(g['target_amount'])
        if 'current_amount' in g and g['current_amount'] is not None: g['current_amount'] = float(g['current_amount'])

    export_data = {
        'user': user,
        'transactions': transactions,
        'budgets': budgets,
        'goals': goals
    }
    
    json_data = json.dumps(export_data, default=str, indent=2)
    
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-disposition": "attachment; filename=SmartSpend_Data_Export.json"}
    )

@reports_bp.route('/export_raw_csv', methods=['GET'])
@token_required
def export_raw_csv():
    db = get_db()
    user_id = request.current_user['user_id']
    transactions = db.get_transactions(user_id, limit=10000)
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Category', 'Amount', 'Type', 'Date', 'Created At'])
    
    for t in transactions:
        cw.writerow([
            t.get('id', ''),
            t.get('name', ''),
            t.get('category', ''),
            float(t.get('amount', 0)),
            t.get('type', ''),
            str(t.get('date', '')),
            str(t.get('created_at', ''))
        ])
        
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=SmartSpend_Transactions.csv"}
    )

@reports_bp.route('/export_budget_csv', methods=['GET'])
@token_required
def export_budget_csv():
    db = get_db()
    user_id = request.current_user['user_id']
    budgets = db.get_budgets(user_id)
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Category', 'Budget Amount', 'Created At'])
    
    for b in budgets:
        cw.writerow([
            b.get('category', ''),
            float(b.get('amount', 0)),
            str(b.get('created_at', ''))
        ])
        
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=SmartSpend_Budgets.csv"}
    )

@reports_bp.route('/export_goals_csv', methods=['GET'])
@token_required
def export_goals_csv():
    db = get_db()
    user_id = request.current_user['user_id']
    goals = db.get_goals(user_id)
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Goal Name', 'Target Amount', 'Current Amount', 'Created At'])
    
    for g in goals:
        cw.writerow([
            g.get('name', ''),
            float(g.get('target_amount', 0)),
            float(g.get('current_amount', 0)),
            str(g.get('created_at', ''))
        ])
        
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=SmartSpend_Goals.csv"}
    )
