import requests

base = "http://127.0.0.1:5000/api"

# Register
requests.post(f"{base}/auth/register", json={"email": "test@test.com", "password": "password", "full_name": "Test User"})

# Login
res = requests.post(f"{base}/auth/login", json={"email": "test@test.com", "password": "password"}).json()
token = res.get("access_token")

if token:
    headers = {"Authorization": f"Bearer {token}"}
    # Billing
    b = requests.post(f"{base}/billing/seed", headers=headers)
    print("Seed:", b.status_code, b.text)
else:
    print("Login failed:", res)
