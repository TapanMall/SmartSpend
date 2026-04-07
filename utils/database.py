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
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False
    
    def fetch_one(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
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
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
    
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
        return self.execute(query, (user_id, name, category, amount, type_, icon, date))
    
    def delete_transaction(self, tx_id, user_id):
        query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
        return self.execute(query, (tx_id, user_id))
