import pytest
from app import app as flask_app
from utils.database import Database

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "DB_NAME": "smartspend_test"
    })
    
    with flask_app.app_context():
        # Setup testing database
        db = Database(db_name="smartspend_test")
        db.init_pool()
        db.execute("DROP TABLE IF EXISTS transactions, categories, budgets, goals, user_billing, user_payment_methods, user_invoices, chat_history, users;")
        db.initialize_db()
        flask_app.config['DB'] = db
        
    yield flask_app
    
    with flask_app.app_context():
        db = flask_app.config['DB']
        db.execute("DROP TABLE IF EXISTS transactions, categories, budgets, goals, user_billing, user_payment_methods, user_invoices, chat_history, users;")

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()