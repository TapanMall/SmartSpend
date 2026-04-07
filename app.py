from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import json

# Fix: Import variables directly instead of Config class which does not exist in config.py
from config import SECRET_KEY, DEBUG, PORT, CORS_ORIGINS
from utils.auth import token_required, generate_token
from utils.database import Database

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize database
db = Database()

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Main routes
@app.route('/')
@app.route('/home')
def index():
    return render_template('smartspend.html')

@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')

# API Routes
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Mock authentication (replace with real auth)
        if email and password:
            user_data = {
                'id': 1,
                'email': email,
                'full_name': 'Arjun Kapoor',
                'plan': 'pro'
            }
            token = generate_token(user_data)
            return jsonify({
                'access_token': token,
                'refresh_token': token, # Mock refresh token
                'user': user_data
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        # Mock registration (replace with real auth)
        if email and password and full_name:
            user_data = {
                'id': 2,
                'email': email,
                'full_name': full_name,
                'plan': 'free'
            }
            token = generate_token(user_data)
            return jsonify({
                'access_token': token,
                'refresh_token': token,
                'user': user_data
            })
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/summary')
@token_required
def analytics_summary():
    try:
        # Mock data (replace with real database queries)
        return jsonify({
            'balance': 128450,
            'income': 85000,
            'expenses': 43240,
            'savings_rate': 34
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/', methods=['GET', 'POST'])
@token_required
def transactions():
    try:
        if request.method == 'GET':
            # Mock transactions data
            return jsonify({
                'transactions': [
                    {
                        'id': 1,
                        'name': 'Blue Tokai Coffee',
                        'category': 'Food & Dining',
                        'amount': 580,
                        'type': 'debit',
                        'date': '2024-04-15',
                        'icon': '🍕'
                    },
                    {
                        'id': 2,
                        'name': 'Salary Credit',
                        'category': 'Income',
                        'amount': 85000,
                        'type': 'credit',
                        'date': '2024-04-01',
                        'icon': '💵'
                    }
                ]
            })
        elif request.method == 'POST':
            data = request.get_json()
            # Mock saving transaction
            return jsonify({
                'transaction': {
                    'id': 999,
                    **data
                },
                'message': 'Transaction added successfully'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<int:tx_id>', methods=['DELETE'])
@token_required
def delete_transaction(tx_id):
    try:
        # Mock deletion
        return jsonify({'message': 'Transaction deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/', methods=['POST'])
@token_required
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Mock AI response
        responses = {
            'balance': "Your total balance is ₹1,28,450. You've saved 34% of your income this month!",
            'spend': "You've spent ₹43,240 so far in April. Your biggest expense is Shopping (₹9,800).",
            'default': "That's a great question! Based on your spending patterns, you're doing well with your savings."
        }
        
        response = responses.get('balance', responses['default'])
        if 'spend' in message.lower():
            response = responses['spend']
        
        return jsonify({'reply': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Additional helper endpoints for auxiliary routes to render html
@app.route('/<page>.html')
def render_auxiliary_pages(page):
    valid_pages = ['about', 'blog', 'careers', 'contact', 'press', 'privacy', 'terms', 'cookies', 'gdpr', 'security']
    if page in valid_pages:
        return render_template(f'{page}.html')
    return not_found(None)

@app.route('/about')
def about_route(): return render_template('about.html')
@app.route('/contact')
def contact_route(): return render_template('contact.html')
@app.route('/blog')
def blog_route(): return render_template('blog.html')
@app.route('/privacy')
def privacy_route(): return render_template('privacy.html')
@app.route('/terms')
def terms_route(): return render_template('terms.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)