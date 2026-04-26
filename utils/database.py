# Database utilities for SmartSpend
import mysql.connector
from mysql.connector import Error, pooling
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import os

class Database:
    def __init__(self, db_name=None, pool_size: Optional[int] = None):
        self.pool_name = "smartspend_pool"
        # Default conservatively to avoid exhausting MySQL connections on dev/test.
        env_pool_size = os.getenv("DB_POOL_SIZE")
        default_pool_size = int(env_pool_size) if (env_pool_size and env_pool_size.isdigit()) else 5
        self.pool_size = pool_size or default_pool_size
        self.pool = None
        self.db_name = db_name or DB_NAME
        
    def init_pool(self):
        try:
            # Create DB if not exists
            temp_conn = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASSWORD
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            temp_cursor.close()
            temp_conn.close()

            # Create connection pool
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                pool_reset_session=True,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=self.db_name
            )
            return True
        except Error as e:
            print(f"Error creating connection pool: {e}")
            return False

    def execute(self, query: str, params: Optional[Tuple] = None) -> Any:
        if not self.pool:
            if not self.init_pool():
                print("Failed to initialize database pool.")
                return False
            
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor.lastrowid if cursor.lastrowid else True
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Error executing query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict]:
        if not self.pool:
            if not self.init_pool():
                print("Failed to initialize database pool.")
                return None
            
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            connection.commit() # Ensure fresh read
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        if not self.pool:
            if not self.init_pool():
                print("Failed to initialize database pool.")
                return []
            
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            connection.commit() # Ensure fresh read
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def initialize_db(self):
        """Create initial database tables if they don't exist"""
        if not self.pool:
            if not self.init_pool():
                print("Failed to initialize database pool.")
                return False
            
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor()
            # Users Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    phone VARCHAR(20) DEFAULT '',
                    currency VARCHAR(50) DEFAULT '₹ INR — Indian Rupee',
                    plan VARCHAR(50) DEFAULT 'starter',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Catch errors if columns already exist
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20) DEFAULT ''")
            except Error:
                pass
                
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN currency VARCHAR(50) DEFAULT '₹ INR — Indian Rupee'")
            except Error:
                pass

            try:
                cursor.execute("ALTER TABLE users ADD COLUMN profile_photo LONGTEXT")
            except Error:
                pass
            
            # Transactions Table
            cursor.execute("""
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
            
            # Add indexes
            try:
                cursor.execute("CREATE INDEX idx_tx_date ON transactions(date)")
            except Error:
                pass
            try:
                cursor.execute("CREATE INDEX idx_tx_category ON transactions(category)")
            except Error:
                pass
            
            # Categories Table (Optional metadata)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    icon VARCHAR(20),
                    type ENUM('expense', 'income') DEFAULT 'expense'
                )
            """)

            # Budgets Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    category VARCHAR(100) NOT NULL,
                    budget_amount DECIMAL(15, 2) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            # Ensure one budget per category per user
            try:
                cursor.execute("ALTER TABLE budgets ADD CONSTRAINT uq_budgets_user_category UNIQUE (user_id, category)")
            except Error:
                pass

            # Goals Table
            cursor.execute("""
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

            # Loans Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS loans (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(100) DEFAULT 'Personal',
                    total_amount DECIMAL(15, 2) NOT NULL,
                    emi_amount DECIMAL(15, 2) DEFAULT 0,
                    outstanding_amount DECIMAL(15, 2) DEFAULT 0,
                    interest_rate DECIMAL(5, 2) DEFAULT 0,
                    start_date DATE,
                    end_date DATE,
                    tenure_months INT DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            try:
                cursor.execute("ALTER TABLE loans ADD COLUMN start_date DATE")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE loans ADD COLUMN end_date DATE")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE loans ADD COLUMN tenure_months INT DEFAULT 0")
            except Error:
                pass

            # EMI History Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emi_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    loan_id INT,
                    amount_paid DECIMAL(15, 2) NOT NULL,
                    principal_paid DECIMAL(15, 2) DEFAULT 0,
                    interest_paid DECIMAL(15, 2) DEFAULT 0,
                    payment_date DATE NOT NULL,
                    status ENUM('PAID', 'PENDING', 'MISSED') DEFAULT 'PAID',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE CASCADE
                )
            """)
            
            # Billing Config Table
            cursor.execute("""
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_payment_methods (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    method_type ENUM('CARD', 'UPI', 'QR') DEFAULT 'CARD',
                    card_last4 VARCHAR(4),
                    upi_id VARCHAR(255),
                    exp_month INT,
                    exp_year INT,
                    brand VARCHAR(50),
                    is_default BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # Migrate existing user_payment_methods table
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN method_type ENUM('CARD', 'UPI', 'QR') DEFAULT 'CARD'")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN upi_id VARCHAR(255)")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN card_last4 VARCHAR(4)")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN exp_month INT")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN exp_year INT")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN brand VARCHAR(50)")
            except Error:
                pass
            try:
                cursor.execute("ALTER TABLE user_payment_methods ADD COLUMN is_default BOOLEAN DEFAULT FALSE")
            except Error:
                pass

            # Invoices Table
            cursor.execute("""
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
            
            # Chat History Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    role ENUM('user', 'assistant', 'system') NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)

            # Investments Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS investments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(100) DEFAULT 'Stocks',
                    amount DECIMAL(15, 2) NOT NULL,
                    date DATE NOT NULL,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
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
            
            cursor.executemany(
                "INSERT IGNORE INTO categories (name, icon, type) VALUES (%s, %s, %s)",
                default_categories
            )
            
            connection.commit()
            print("Database initialized successfully.")
            return True
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Error initializing database: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        return self.fetch_one(query, (email,))
    
    def create_user(self, email, password_hash, full_name):
        query = """
            INSERT INTO users (email, password_hash, full_name, plan, created_at)
            VALUES (%s, %s, %s, 'starter', NOW())
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
            LIMIT 12
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

    def update_user_profile(self, user_id, full_name, email, phone='', currency='₹ INR — Indian Rupee'):
        query = "UPDATE users SET full_name = %s, email = %s, phone = %s, currency = %s WHERE id = %s"
        return self.execute(query, (full_name, email, phone, currency, user_id))

    def update_user_password(self, user_id, password_hash):
        query = "UPDATE users SET password_hash = %s WHERE id = %s"
        return self.execute(query, (password_hash, user_id))

    def delete_user_account(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        return self.execute(query, (user_id,))

    def get_budgets(self, user_id):
        query = "SELECT id, user_id, category, budget_amount as amount, created_at FROM budgets WHERE user_id = %s"
        return self.fetch_all(query, (user_id,))

    def get_budgets_with_spending(self, user_id):
        query = """
            SELECT b.id, b.user_id, b.category, b.budget_amount as amount, b.created_at,
                   COALESCE(SUM(t.amount), 0) as spent
            FROM budgets b
            LEFT JOIN transactions t ON b.user_id = t.user_id 
                                     AND b.category = t.category 
                                     AND t.type = 'debit'
                                     AND YEAR(t.date) = YEAR(CURRENT_DATE()) 
                                     AND MONTH(t.date) = MONTH(CURRENT_DATE())
            WHERE b.user_id = %s
            GROUP BY b.id, b.user_id, b.category, b.budget_amount, b.created_at
        """
        return self.fetch_all(query, (user_id,))

    def create_budget(self, user_id, category, amount):
        query = "INSERT INTO budgets (user_id, category, budget_amount) VALUES (%s, %s, %s)"
        b_id = self.execute(query, (user_id, category, amount))
        if b_id:
            return self.fetch_one("SELECT id, user_id, category, budget_amount as amount, created_at FROM budgets WHERE id = %s", (b_id,))
        return None

    def update_budget(self, user_id, budget_id, category, amount):
        query = "UPDATE budgets SET category = %s, budget_amount = %s WHERE id = %s AND user_id = %s"
        self.execute(query, (category, amount, budget_id, user_id))
        return self.fetch_one("SELECT id, user_id, category, budget_amount as amount, created_at FROM budgets WHERE id = %s AND user_id = %s", (budget_id, user_id))

    def delete_budget(self, user_id, budget_id):
        query = "DELETE FROM budgets WHERE id = %s AND user_id = %s"
        self.execute(query, (budget_id, user_id))
        return True

    def get_goals(self, user_id):
        query = "SELECT * FROM goals WHERE user_id = %s"
        return self.fetch_all(query, (user_id,))

    def create_goal(self, user_id, name, target_amount, current_amount=0):
        query = "INSERT INTO goals (user_id, name, target_amount, current_amount) VALUES (%s, %s, %s, %s)"
        g_id = self.execute(query, (user_id, name, target_amount, current_amount))
        if g_id:
            return self.fetch_one("SELECT * FROM goals WHERE id = %s", (g_id,))
        return None

    def update_goal_progress(self, goal_id, current_amount):
        query = "UPDATE goals SET current_amount = %s WHERE id = %s"
        return self.execute(query, (current_amount, goal_id))

    def delete_goal(self, user_id, goal_id):
        query = "DELETE FROM goals WHERE id = %s AND user_id = %s"
        self.execute(query, (goal_id, user_id))
        return True

    # Investment Methods
    def get_investments(self, user_id):
        query = "SELECT * FROM investments WHERE user_id = %s ORDER BY date DESC"
        return self.fetch_all(query, (user_id,))

    def create_investment(self, user_id, name, type, amount, date, notes=''):
        query = "INSERT INTO investments (user_id, name, type, amount, date, notes) VALUES (%s, %s, %s, %s, %s, %s)"
        inv_id = self.execute(query, (user_id, name, type, amount, date, notes))
        if inv_id:
            return self.fetch_one("SELECT * FROM investments WHERE id = %s", (inv_id,))
        return None

    def delete_investment(self, investment_id, user_id):
        query = "DELETE FROM investments WHERE id = %s AND user_id = %s"
        if not self.pool:
            if not self.init_pool():
                print("Failed to initialize database pool.")
                return False

        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, (investment_id, user_id))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            if connection:
                connection.rollback()
            print(f"Error executing query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # Net Worth Calculation
    def get_net_worth_stats(self, user_id):
        """Aggregate data for the Net Worth view"""
        # 1. Total Balance from transactions (Credits - Debits)
        balance_query = """
            SELECT 
                SUM(CASE WHEN type = 'credit' THEN amount ELSE 0 END) - 
                SUM(CASE WHEN type = 'debit' THEN amount ELSE 0 END) as balance
            FROM transactions 
            WHERE user_id = %s
        """
        balance_res = self.fetch_one(balance_query, (user_id,))
        total_balance = float(balance_res['balance'] or 0) if balance_res else 0

        # 2. Total Investments
        inv_query = "SELECT SUM(amount) as total FROM investments WHERE user_id = %s"
        inv_res = self.fetch_one(inv_query, (user_id,))
        total_investments = float(inv_res['total'] or 0) if inv_res else 0

        # 3. Total Liabilities (Outstanding Loans)
        loan_query = "SELECT SUM(outstanding_amount) as total FROM loans WHERE user_id = %s"
        loan_res = self.fetch_one(loan_query, (user_id,))
        total_liabilities = float(loan_res['total'] or 0) if loan_res else 0

        total_assets = total_balance + total_investments
        net_worth = total_assets - total_liabilities

        return {
            'total_balance': total_balance,
            'total_investments': total_investments,
            'total_liabilities': total_liabilities,
            'total_assets': total_assets,
            'net_worth': net_worth,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
