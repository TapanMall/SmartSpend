import json

def test_register_and_login(client):
    # Register
    res = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'full_name': 'Test User'
    })
    assert res.status_code == 201
    data = json.loads(res.data)
    assert 'access_token' in data
    
    # Login
    res2 = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert res2.status_code == 200
    data2 = json.loads(res2.data)
    assert 'access_token' in data2