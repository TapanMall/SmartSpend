from flask import Blueprint, request, jsonify
from utils.database import Database
from utils.auth import token_required
from models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)
db = Database()

@transactions_bp.route('/', methods=['GET', 'POST'])
@token_required
def transactions():
    try:
        user_id = request.current_user['user_id']
        
        if request.method == 'GET':
            limit = request.args.get('limit', 50, type=int)
            txs = db.get_transactions(user_id, limit)
            return jsonify({
                'transactions': Transaction.format_transactions(txs)
            })
            
        elif request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            category = data.get('category', 'Others')
            amount = data.get('amount')
            type_ = data.get('type')  # 'debit' or 'credit'
            icon = data.get('icon', '📝')
            date = data.get('date')
            
            if not all([name, amount, type_, date]):
                return jsonify({'error': 'Missing required fields'}), 400
                
            tx = db.create_transaction(user_id, name, category, amount, type_, icon, date)
            if tx:
                return jsonify({
                    'message': 'Transaction added successfully',
                    'transaction': Transaction.format_transaction(tx)
                }), 201
            else:
                return jsonify({'error': 'Failed to add transaction'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:tx_id>', methods=['DELETE'])
@token_required
def delete_transaction(tx_id):
    try:
        user_id = request.current_user['user_id']
        if db.delete_transaction(tx_id, user_id):
            return jsonify({'message': 'Transaction deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete transaction'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
