import json
from models.user import User

def test_create_transaction(client, app):
    # First register a user
    client.post('/api/auth/register', json={
        'email': 'tx@example.com',
        'password': 'password123',
        'full_name': 'Tx User'
    })
    
    # Login to get token
    res = client.post('/api/auth/login', json={
        'email': 'tx@example.com',
        'password': 'password123'
    })
    token = json.loads(res.data)['access_token']
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Create valid transaction
    res2 = client.post('/api/transactions/', json={
        'name': 'Groceries',
        'category': 'Food',
        'amount': 500,
        'type': 'debit',
        'date': '2023-01-01'
    }, headers=headers)
    assert res2.status_code == 201
    
    # Try invalid amount (negative)
    res3 = client.post('/api/transactions/', json={
        'name': 'Invalid',
        'category': 'Food',
        'amount': -100,
        'type': 'debit',
        'date': '2023-01-01'
    }, headers=headers)
    assert res3.status_code == 400
