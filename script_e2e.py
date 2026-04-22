import requests
import random
from datetime import datetime

base = "http://127.0.0.1:5000/api"

def test_flow():
    print("--- Starting Full E2E Test ---")
    
    # 1. Register
    email = f"test_{random.randint(1000,9999)}@test.com"
    reg = requests.post(f"{base}/auth/register", json={"email": email, "password": "pass", "full_name": "Test Flow"})
    print("Register:", reg.status_code, reg.text)
    
    # 2. Login
    login = requests.post(f"{base}/auth/login", json={"email": email, "password": "pass"}).json()
    token = login.get("access_token")
    if not token:
        print("Login failed")
        return
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Transactions
    tx = requests.post(f"{base}/transactions/", headers=headers, json={"name": "Groceries", "category": "Food & Dining", "amount": 150.50, "type": "debit", "date": "2026-04-22"})
    print("Add Tx:", tx.status_code)
    txs = requests.get(f"{base}/transactions/", headers=headers).json()
    print("List Tx:", len(txs.get("transactions", [])))
    
    # 4. Analytics
    analytics = requests.get(f"{base}/analytics/", headers=headers)
    print("Analytics Status:", analytics.status_code)
    print("Analytics Data:", analytics.text)
    
    # 5. Budgets
    b_add = requests.post(f"{base}/budgets/", headers=headers, json={"category": "Food & Dining", "amount": 500})
    print("Add Budget:", b_add.status_code)
    bs = requests.get(f"{base}/budgets/", headers=headers).json()
    print("List Budgets:", len(bs.get("budgets", [])))
    
    # 6. Goals
    g_add = requests.post(f"{base}/goals/", headers=headers, json={"name": "New Car", "target_amount": 20000})
    print("Add Goal:", g_add.status_code)
    gs = requests.get(f"{base}/goals/", headers=headers).json()
    print("List Goals:", len(gs.get("goals", [])))
    
    # 7. Loans
    l_add = requests.post(f"{base}/loans/", headers=headers, json={"name": "Home Loan", "type": "Home", "total_amount": 50000, "emi_amount": 1000, "outstanding_amount": 45000, "interest_rate": 7.5})
    print("Add Loan:", l_add.status_code)
    ls = requests.get(f"{base}/loans/", headers=headers).json()
    print("List Loans:", len(ls.get("loans", [])))
    
    # 8. Billing
    bill = requests.post(f"{base}/billing/seed", headers=headers)
    print("Seed Billing:", bill.status_code)
    bills = requests.get(f"{base}/billing/", headers=headers).json()
    print("List Billing Invoices:", len(bills.get("invoices", [])))

    print("--- E2E Test Completed ---")

test_flow()
