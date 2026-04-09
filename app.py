from flask import Flask, request, jsonify, render_template, send_from_directory, Response, stream_with_context
from flask_cors import CORS
import os
from datetime import datetime
import json
import re
from openai import OpenAI

# Fix: Import variables directly instead of Config class which does not exist in config.py
from config import SECRET_KEY, DEBUG, PORT, CORS_ORIGINS, NVIDIA_API_KEY

from utils.auth import token_required, generate_token
from utils.database import Database

app = Flask(__name__)
CORS(app, origins=CORS_ORIGINS)
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize database
db = Database()
db.initialize_db()

# Register Blueprints
from routes.auth import auth_bp
from routes.transactions import transactions_bp
from routes.analytics import analytics_bp
from routes.budgets import budgets_bp
from routes.goals import goals_bp
from routes.billing import billing_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
app.register_blueprint(goals_bp, url_prefix='/api/goals')
app.register_blueprint(billing_bp, url_prefix='/api/billing')

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

nvidia_client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

@app.route('/api/chat/', methods=['POST'])
@token_required
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'reply': 'Please type a message!'}), 400

        user_id = request.current_user['user_id']
        summary = db.get_analytics_summary(user_id)

        # Get user's actual name from DB
        user_info = db.fetch_one("SELECT full_name FROM users WHERE id = %s", (user_id,))
        user_name = (user_info.get('full_name') or 'there').split()[0]  # First name only

        system_prompt = (
            f"You are SmartSpend AI, a smart, warm, and proactive personal finance assistant — like a knowledgeable friend who's also a financial advisor. "
            f"The user's name is {user_name}. Address them by first name occasionally to keep it personal. "
            f"Their financial snapshot this month: Balance ₹{summary['balance']:,.2f} | "
            f"Income ₹{summary['income']:,.2f} | Expenses ₹{summary['expenses']:,.2f} | "
            f"Savings Rate: {summary.get('savings_rate', 0)}%. "
            f"Personality rules: "
            f"1. Be conversational, warm, and encouraging — never robotic. "
            f"2. Give specific, actionable advice based on their actual numbers. "
            f"3. Use ₹ for all currency amounts. "
            f"4. Use light markdown: **bold** for key numbers, bullet points for lists. "
            f"5. If they're overspending, be empathetic — don't lecture. "
            f"6. Keep responses concise (3-5 sentences max) unless they ask for details. "
            f"7. End with a helpful follow-up question or tip when appropriate."
        )

        def generate():
            """Stream SSE chunks to the client."""
            try:
                completion = nvidia_client.chat.completions.create(
                    model="qwen/qwen3-next-80b-a3b-instruct",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.6,
                    top_p=0.7,
                    max_tokens=4096,
                    stream=True
                )
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta is not None:
                        # Strip think tags inline
                        delta = re.sub(r'<think>.*?</think>', '', delta, flags=re.DOTALL)
                        if delta:
                            yield f"data: {json.dumps({'token': delta})}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                print(f"[AI Stream Error] {e}")
                # Fallback — send a smart reply based on keywords
                if 'balance' in message.lower():
                    fb = f"Your balance is ₹{summary['balance']:,.2f}."
                elif 'spend' in message.lower() or 'expense' in message.lower():
                    fb = f"You've spent ₹{summary['expenses']:,.2f} this month."
                elif 'income' in message.lower():
                    fb = f"Your income this month is ₹{summary['income']:,.2f}."
                else:
                    fb = f"Your balance is ₹{summary['balance']:,.2f}. How can I help?"
                yield f"data: {json.dumps({'token': fb})}\n\n"
                yield "data: [DONE]\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    except Exception as e:
        print(f"[Chat Outer Error] {e}")
        return jsonify({'reply': "I'm having a momentary issue. Please try again!"}), 200


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