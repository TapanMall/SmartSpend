import pytest
from app import create_app
from utils.database import Database

@pytest.fixture
def app():
    flask_app = create_app(init_db=False)
    flask_app.config.update({
        "TESTING": True,
        "DB_NAME": "smartspend_test"
    })
    
    with flask_app.app_context():
        # Setup testing database
        db = Database(db_name="smartspend_test", pool_size=3)
        db.init_pool()
        db.execute("SET FOREIGN_KEY_CHECKS = 0;")
        db.execute("DROP TABLE IF EXISTS emi_history, transactions, investments, categories, budgets, goals, user_billing, user_payment_methods, user_invoices, chat_history, loans, users;")
        db.execute("SET FOREIGN_KEY_CHECKS = 1;")
        db.initialize_db()
        flask_app.config['DB'] = db
        
    yield flask_app
    
    with flask_app.app_context():
            db = flask_app.config['DB']
            db.execute("SET FOREIGN_KEY_CHECKS = 0;")
            db.execute("DROP TABLE IF EXISTS emi_history, transactions, investments, categories, budgets, goals, user_billing, user_payment_methods, user_invoices, chat_history, loans, users;")
            db.execute("SET FOREIGN_KEY_CHECKS = 1;")

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
