from flask import Blueprint, request, jsonify, current_app
from utils.database import Database
from utils.auth import token_required
from models.transaction import Transaction
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image

transactions_bp = Blueprint('transactions', __name__)

def get_db():
    return current_app.config['DB']

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@transactions_bp.route('/upload', methods=['POST'])
@token_required
def upload_receipt():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Check size (reading stream length then resetting)
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > MAX_CONTENT_LENGTH:
            return jsonify({'error': 'File too large. Maximum 5MB.'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # In a real scenario we might save this or just process in memory
            try:
                img = Image.open(file)
                text = pytesseract.image_to_string(img)
                # Mock parsing logic based on OCR text
                amount = 0
                import re
                amounts = re.findall(r'\d+\.\d{2}', text)
                if amounts:
                    amount = max([float(a) for a in amounts])
                
                return jsonify({
                    'message': 'File processed successfully',
                    'extracted_amount': amount,
                    'raw_text': text
                }), 200
            except Exception as inner_e:
                current_app.logger.error(f"OCR Error: {str(inner_e)}")
                return jsonify({'error': 'Failed to process image for OCR'}), 500
        
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@transactions_bp.route('/', methods=['GET', 'POST'])
@token_required
def transactions():
    try:
        db = get_db()
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
            date_str = data.get('date')
            
            if not all([name, amount, type_, date_str]):
                return jsonify({'error': 'Missing required fields'}), 400
                
            try:
                amount_val = float(amount)
                if amount_val <= 0:
                    return jsonify({'error': 'Amount must be positive'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid amount format'}), 400
                
            try:
                tx_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if tx_date > datetime.now().date():
                    return jsonify({'error': 'Transaction date cannot be in the future'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
                
            tx = db.create_transaction(user_id, name, category, amount_val, type_, icon, date_str)
            if tx:
                cache = current_app.config.get('CACHE')
                if cache:
                    cache.delete(f'analytics_summary_{user_id}')
                return jsonify({
                    'message': 'Transaction added successfully',
                    'transaction': Transaction.format_transaction(tx)
                }), 201
            else:
                return jsonify({'error': 'Failed to add transaction'}), 500
                
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500

@transactions_bp.route('/<int:tx_id>', methods=['DELETE'])
@token_required
def delete_transaction(tx_id):
    try:
        db = get_db()
        user_id = request.current_user['user_id']
        if db.delete_transaction(tx_id, user_id):
            cache = current_app.config.get('CACHE')
            if cache:
                cache.delete(f'analytics_summary_{user_id}')
            return jsonify({'message': 'Transaction deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete transaction'}), 500
            
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'error': 'An internal server error occurred'}), 500
