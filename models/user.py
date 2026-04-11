from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, password_hash):
        return check_password_hash(password_hash, password)

    @staticmethod
    def format_user_data(user):
        """Format user data for API response (remove password hash)"""
        if not user:
            return None
        return {
            'id': user['id'],
            'email': user['email'],
            'full_name': user.get('full_name'),
            'phone': user.get('phone', ''),
            'currency': user.get('currency', '₹ INR — Indian Rupee'),
            'plan': user.get('plan', 'starter'),
            'created_at': user.get('created_at').isoformat() if hasattr(user.get('created_at'), 'isoformat') else user.get('created_at')
        }
