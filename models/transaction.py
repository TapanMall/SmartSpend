from decimal import Decimal

class Transaction:
    @staticmethod
    def format_transaction(tx):
        """Format a single transaction for API response"""
        if not tx:
            return None
            
        # Convert Decimal to float for JSON serializability
        amount = float(tx['amount']) if isinstance(tx['amount'], Decimal) else tx['amount']
        
        # Format date if it's a datetime object
        date = tx['date'].isoformat() if hasattr(tx.get('date'), 'isoformat') else tx.get('date')
        created_at = tx['created_at'].isoformat() if hasattr(tx.get('created_at'), 'isoformat') else tx.get('created_at')
        
        return {
            'id': tx['id'],
            'user_id': tx['user_id'],
            'name': tx['name'],
            'category': tx['category'],
            'amount': amount,
            'type': tx['type'],
            'icon': tx['icon'],
            'date': date,
            'created_at': created_at
        }

    @staticmethod
    def format_transactions(transactions):
        """Format a list of transactions for API response"""
        return [Transaction.format_transaction(tx) for tx in transactions]
