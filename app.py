from flask import Flask, request, jsonify, render_template, send_from_directory, Response, stream_with_context, current_app
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix
from whitenoise import WhiteNoise
import os
from datetime import datetime
import json
import re
from openai import OpenAI

# Fix: Import variables directly instead of Config class which does not exist in config.py
from config import SECRET_KEY, DEBUG, PORT, CORS_ORIGINS, NVIDIA_API_KEY, JWT_SECRET

from utils.auth import token_required, generate_token
from utils.database import Database

def create_app(*, init_db: bool = True) -> Flask:
    app = Flask(__name__)
    # For production readiness, handle proxies and use whitenoise for static files
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')

    CORS(app, origins=CORS_ORIGINS.split(','), supports_credentials=True)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SWAGGER'] = {'title': 'SmartSpend API', 'uiversion': 3}

    # Fail fast on insecure JWT configuration (except tests).
    if not app.config.get('TESTING') and not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is missing. Set JWT_SECRET in your environment.")

    # Initialize extensions
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["2000 per day", "500 per hour"],
        storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
    )
    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
    swagger = Swagger(app)
    app.config['CACHE'] = cache
    app.config['LIMITER'] = limiter

    # Initialize database and store in app context for dependency injection
    if init_db:
        db = Database()
        db.initialize_db()
        app.config['DB'] = db

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.transactions import transactions_bp
    from routes.analytics import analytics_bp
    from routes.budgets import budgets_bp
    from routes.goals import goals_bp
    from routes.billing import billing_bp
    from routes.reports import reports_bp
    from routes.loans import loans_bp
    from routes.investments import investments_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(loans_bp, url_prefix='/api/loans')
    app.register_blueprint(investments_bp, url_prefix='/api/investments')

    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        return jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }), e.code

    # Serve static files (handled by whitenoise in production, but keeping this for development if needed)
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

    @app.route('/onboarding')
    def onboarding():
        return render_template('onboarding.html')

    nvidia_client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )

    @app.route('/api/chat/', methods=['POST'])
    @token_required
    @limiter.limit("5 per minute")
    def chat():
        """
        AI Chat Endpoint
        ---
        tags:
          - AI
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                message:
                  type: string
        responses:
          200:
            description: Stream of AI response
        """
        try:
            data = request.get_json()
            message = (data or {}).get('message', '').strip()
            if not message:
                return jsonify({'reply': 'Please type a message!'}), 400
            if len(message) > 1000:
                return jsonify({'error': 'Message too long. Maximum 1000 characters.'}), 400

            user_id = request.current_user['user_id']

            db = current_app.config['DB']
            summary = db.get_analytics_summary(user_id)

            # Get user's actual name from DB
            user_info = db.fetch_one("SELECT full_name FROM users WHERE id = %s", (user_id,))
            user_name = ((user_info or {}).get('full_name') or 'there').split()[0]  # First name only

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

            # Fetch chat history
            history_records = db.fetch_all(
                "SELECT role, content FROM chat_history WHERE user_id = %s ORDER BY created_at ASC LIMIT 10",
                (user_id,)
            )

            messages = [{"role": "system", "content": system_prompt}]
            for rec in history_records:
                messages.append({"role": rec['role'], "content": rec['content']})

            # Append current message wrapped in user_input to prevent injection
            messages.append({"role": "user", "content": f"<user_input>\n{message}\n</user_input>"})

            # Save user message to history
            db.execute(
                "INSERT INTO chat_history (user_id, role, content) VALUES (%s, %s, %s)",
                (user_id, 'user', message)
            )

            def generate():
                """Stream SSE chunks to the client with safe <think> tag stripping."""
                try:
                    completion = nvidia_client.chat.completions.create(
                        model="qwen/qwen3-next-80b-a3b-instruct",
                        messages=messages,
                        temperature=0.6,
                        top_p=0.7,
                        max_tokens=4096,
                        stream=True
                    )
                    buffer = ""
                    in_think = False
                    full_response = ""

                    for chunk in completion:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            buffer += delta

                            # Process buffer to strip <think> blocks
                            while True:
                                if not in_think:
                                    think_start = buffer.find('<think>')
                                    if think_start != -1:
                                        # Yield text before <think>
                                        if think_start > 0:
                                            text_to_yield = buffer[:think_start]
                                            full_response += text_to_yield
                                            yield f"data: {json.dumps({'token': text_to_yield})}\n\n"
                                        buffer = buffer[think_start + 7:]
                                        in_think = True
                                    else:
                                        # Yield text but keep last 7 chars just in case a <think> tag is partially formed
                                        if len(buffer) > 7:
                                            text_to_yield = buffer[:-7]
                                            full_response += text_to_yield
                                            yield f"data: {json.dumps({'token': text_to_yield})}\n\n"
                                            buffer = buffer[-7:]
                                        break
                                else:
                                    think_end = buffer.find('</think>')
                                    if think_end != -1:
                                        buffer = buffer[think_end + 8:]
                                        in_think = False
                                    else:
                                        # Still inside think block, wait for </think>
                                        break

                    # Flush remaining buffer if not in think block
                    if buffer and not in_think:
                        # Remove any partial <think tags that might be at the end
                        clean_buffer = re.sub(r'<think>?.*', '', buffer, flags=re.DOTALL)
                        if clean_buffer:
                            full_response += clean_buffer
                            yield f"data: {json.dumps({'token': clean_buffer})}\n\n"

                    # Save assistant response to history
                    if full_response:
                        db.execute(
                            "INSERT INTO chat_history (user_id, role, content) VALUES (%s, %s, %s)",
                            (user_id, 'assistant', full_response)
                        )

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
            current_app.logger.error(f"[Chat Outer Error] {e}")
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

    return app


# WSGI entrypoint (gunicorn, etc.)
app = create_app(init_db=True)
limiter = app.config.get('LIMITER')
cache = app.config.get('CACHE')

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)