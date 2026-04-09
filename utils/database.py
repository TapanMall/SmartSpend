# Database utilities for SmartSpend
import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        try:
            # First try connecting without a specific database to ensure we can create it if missing
            temp_conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            temp_cursor.close()
            temp_conn.close()

            # Now connect to the actual database
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
    
    def execute(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.lastrowid if self.cursor.lastrowid else True
        except Error as e:
            print(f"Error executing query: {e}")
            raise  # Raise the error so it can be caught by the route handler
    
    def fetch_one(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            self.connection.commit()  # Ensure fresh read
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            self.connection.commit()  # Ensure fresh read
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
    
    def initialize_db(self):
        """Create initial database tables if they don't exist"""
        if not self.connect():
            print("Failed to connect for database initialization.")
            return False
            
        try:
            # Users Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    plan VARCHAR(50) DEFAULT 'free',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Transactions Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100),
                    amount DECIMAL(15, 2) NOT NULL,
                    type ENUM('debit', 'credit') NOT NULL,
                    icon VARCHAR(20),
                    date DATE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Categories Table (Optional metadata)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    icon VARCHAR(20),
                    type ENUM('expense', 'income') DEFAULT 'expense'
                )
            """)

            # Budgets Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    category VARCHAR(100) NOT NULL,
                    amount DECIMAL(15, 2) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # Goals Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    name VARCHAR(255) NOT NULL,
                    target_amount DECIMAL(15, 2) NOT NULL,
                    current_amount DECIMAL(15, 2) DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            # Billing Config Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_billing (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT UNIQUE,
                    plan_type VARCHAR(50) DEFAULT 'STARTER',
                    billing_email VARCHAR(255) DEfAULT '',
                    address VARCHAR(255) DEFAULT '',
                    country VARCHAR(100) DEFAULT '',
                    business_tax_id VARCHAR(100) DEFAULT '',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # Payment Methods Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_payment_methods (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    card_last4 VARCHAR(4),
                    exp_month INT,
                    exp_year INT,
                    brand VARCHAR(50),
                    is_default BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # Invoices Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_invoices (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    amount DECIMAL(15, 2) NOT NULL,
                    invoice_number VARCHAR(100) UNIQUE,
                    status ENUM('PAID', 'PENDING', 'FAILED') DEFAULT 'PAID',
                    date_issued DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Default categories
            default_categories = [
                ('Food & Dining', '🍕', 'expense'),
                ('Transport', '🚗', 'expense'),
                ('Shopping', '🛍️', 'expense'),
                ('Entertainment', '🎬', 'expense'),
                ('Health', '🏥', 'expense'),
                ('Bills & Utilities', '📱', 'expense'),
                ('Income', '💵', 'income'),
                ('Investment', '📈', 'income'),
                ('Others', '📝', 'expense')
            ]
            
            self.cursor.executemany(
                "INSERT IGNORE INTO categories (name, icon, type) VALUES (%s, %s, %s)",
                default_categories
            )
            
            self.connection.commit()
            print("Database initialized successfully.")
            return True
        except Error as e:
            print(f"Error initializing database: {e}")
            return False
        finally:
            self.disconnect()

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        return self.fetch_one(query, (email,))
    
    def create_user(self, email, password_hash, full_name):
        query = """
            INSERT INTO users (email, password_hash, full_name, created_at)
            VALUES (%s, %s, %s, NOW())
        """
        return self.execute(query, (email, password_hash, full_name))
    
    def get_transactions(self, user_id, limit=50):
        query = """
            SELECT * FROM transactions 
            WHERE user_id = %s 
            ORDER BY date DESC, created_at DESC 
            LIMIT %s
        """
        return self.fetch_all(query, (user_id, limit))
    
    def create_transaction(self, user_id, name, category, amount, type_, icon, date):
        query = """
            INSERT INTO transactions (user_id, name, category, amount, type, icon, date, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        tx_id = self.execute(query, (user_id, name, category, amount, type_, icon, date))
        if tx_id:
            # Fetch the created transaction to return it
            return self.fetch_one("SELECT * FROM transactions WHERE id = %s", (tx_id,))
        return None
    
    def delete_transaction(self, tx_id, user_id):
        query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
        return self.execute(query, (tx_id, user_id))

    def get_analytics_summary(self, user_id):
        """Get summary of income, expenses, and category breakdown"""
        # Overall Summary
        summary_query = """
            SELECT 
                SUM(CASE WHEN type = 'credit' THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END) as expenses,
                COUNT(*) as count
            FROM transactions 
            WHERE user_id = %s
        """
        res = self.fetch_one(summary_query, (user_id,))
        if not res:
            return {'income': 0, 'expenses': 0, 'balance': 0, 'count': 0, 'categories': {}, 'monthly': []}
        
        income = float(res['income'] or 0)
        expenses = float(res['expenses'] or 0)
        count = int(res['count'] or 0)
        balance = income - expenses

        # Category Breakdown
        cat_query = """
            SELECT category, SUM(amount) as total 
            FROM transactions 
            WHERE user_id = %s AND type = 'debit'
            GROUP BY category
        """
        cat_res = self.fetch_all(cat_query, (user_id,))
        categories = {row['category']: float(row['total']) for row in cat_res}

        # Monthly comparison for Bar Chart
        monthly_query = """
            SELECT 
                DATE_FORMAT(date, '%b') as month,
                SUM(CASE WHEN type = 'credit' THEN amount ELSE 0 END) as inc,
                SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END) as exp
            FROM transactions 
            WHERE user_id = %s
            GROUP BY DATE_FORMAT(date, '%Y-%m'), DATE_FORMAT(date, '%b')
            ORDER BY DATE_FORMAT(date, '%Y-%m') DESC
            LIMIT 6
        """
        monthly_res = self.fetch_all(monthly_query, (user_id,))
        for row in monthly_res:
            row['inc'] = float(row['inc'] or 0)
            row['exp'] = float(row['exp'] or 0)
        monthly_data = list(reversed(monthly_res))

        return {
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'count': count,
            'savings_rate': round(((income - expenses) / income * 100), 2) if income > 0 else 0,
            'categories': categories,
            'monthly': monthly_data
        }

    def update_user_profile(self, user_id, full_name, email):
        query = "UPDATE users SET full_name = %s, email = %s WHERE id = %s"
        return self.execute(query, (full_name, email, user_id))

    def get_budgets(self, user_id):
        query = "SELECT id, user_id, category, budget_amount as amount, created_at FROM budgets WHERE user_id = %s"
        return self.fetch_all(query, (user_id,))

    def create_budget(self, user_id, category, amount):
        query = "INSERT INTO budgets (user_id, category, budget_amount) VALUES (%s, %s, %s)"
        b_id = self.execute(query, (user_id, category, amount))
        if b_id:
            return self.fetch_one("SELECT id, user_id, category, budget_amount as amount, created_at FROM budgets WHERE id = %s", (b_id,))
        return None

    def get_goals(self, user_id):
        query = "SELECT * FROM goals WHERE user_id = %s"
        return self.fetch_all(query, (user_id,))

    def create_goal(self, user_id, name, target_amount, current_amount=0):
        query = "INSERT INTO goals (user_id, name, target_amount, current_amount) VALUES (%s, %s, %s, %s)"
        g_id = self.execute(query, (user_id, name, target_amount, current_amount))
        if g_id:
            return self.fetch_one("SELECT * FROM goals WHERE id = %s", (g_id,))
        return None
