<div align="center">

# 💸 SmartSpend

### Your Intelligent Financial Companion

*Track. Analyse. Grow.*

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Flask](https://img.shields.io/badge/Powered%20by-Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Database MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Made with HTML](https://img.shields.io/badge/Made%20with-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Styled with CSS](https://img.shields.io/badge/Styled%20with-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Powered by JS](https://img.shields.io/badge/Powered%20by-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Charts by Chart.js](https://img.shields.io/badge/Charts-Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![AI by NVIDIA](https://img.shields.io/badge/AI-NVIDIA%20NIM-76B900?style=flat-square&logo=nvidia&logoColor=white)](https://build.nvidia.com/)

</div>

---

## 🌟 What is SmartSpend?

**SmartSpend** is a premium, full-featured personal finance dashboard built with a robust **Python Flask** and **MySQL** backend, paired with a stunning vanilla HTML, CSS, and JavaScript frontend. It combines beautiful claymorphism design with powerful financial tracking tools, AI-powered insights, and wealth management features.

Designed for Indian users with ₹ currency formatting, it covers everything from daily expense tracking to investment portfolio management, EMI planning, and net worth analysis.

---

## ✨ Features

### 📊 Core Finance
| Feature | Description |
|---|---|
| **Dashboard Overview** | Live stat cards for balance, income, expenses & savings rate with sparkline charts |
| **Transaction Manager** | Add, filter, search & delete transactions with category tagging |
| **Budget Tracker** | Visual budget bars per category with overspend alerts |
| **Financial Goals** | Progress tracking for savings goals with monthly contribution breakdown |
| **Analytics** | Cash flow trends, category distribution, savings growth & spending heatmap |

### 💼 Wealth Management *(New)*
| Feature | Description |
|---|---|
| **Investments** | Portfolio value tracking, asset allocation doughnut chart & growth line chart |
| **Loans & EMI** | Active loan cards with repayment progress, ROI display & next EMI reminders |
| **Net Worth** | Complete balance sheet (Assets vs. Liabilities) with historical wealth growth |

### 🤖 Intelligence
| Feature | Description |
|---|---|
| **AI Insights** | 4 auto-generated insight cards — alerts, wins, tips & trends |
| **AI Chat Assistant** | Floating chat panel powered by NVIDIA API (with smart local fallback) |
| **Voice Entry** | Hands-free expense logging via voice transcription |
| **OCR Receipt Scan** | Instant data extraction from physical receipt photos |

### 🎨 UI/UX
- 🌙 **Dark / Light Mode** — seamless theme toggling with CSS variables
- 🔔 **Notification Panel** — real-time alerts for budget overruns & milestones
- 📱 **Fully Responsive** — works on mobile, tablet & desktop
- ✨ **Claymorphism Design** — soft shadows, glassmorphism cards & micro-animations
- 🍞 **Toast Notifications** — animated success/error feedback system
- 🗂️ **Collapsible Sidebar** — icon-only mode for more screen real estate

---

## 🛠️ Tech Stack

```text
Frontend       → Semantic HTML5  +  Vanilla CSS3  +  ES6+ JavaScript
Backend        → Python 3 + Flask API + JWT Authentication
Database       → MySQL
Charts         → Chart.js (CDN)
Typography     → Syne (Headings)  ·  DM Sans (Body)  ·  JetBrains Mono (Numbers)
AI Integration → NVIDIA NIM API (Qwen Model)
Icons          → Emoji-native  +  Custom inline SVG
Design System  → CSS Custom Properties (tokens), Claymorphism shadows
```

---

## 📂 Project Structure

```text
SmartSpend-main/
│
├── app.py                   # 🐍 Main Flask Application Entry Point
├── config.py                # ⚙️ Application Configuration
├── recreate_db.py           # 🗄️ Database initialization script
├── requirements.txt         # 📦 Python dependencies
│
├── routes/                  # 🛣️ API Endpoints (Auth, Transactions, etc.)
├── models/                  # 📊 Database models
├── utils/                   # 🛠️ Helper functions (Auth, DB, etc.)
│
├── static/                  # 📂 Static assets (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/               # 📄 HTML Templates
│   ├── smartspend.html      # 🏠 Main Landing Page
│   ├── Dashboard.html       # 📊 Full Finance Dashboard
│   └── ...                  # Other pages (About, Blog, Contact, etc.)
└── README.md                # 📖 You are here
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/SmartSpend.git
cd SmartSpend-main
```

### 2. Set up Backend Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Activate it (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Database
1. Make sure you have **MySQL** installed and running.
2. Copy `.env.example` to `.env` and fill in your database credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=smartspend
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```
3. Initialize the database schema:
```bash
python recreate_db.py
```

### 4. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://localhost:5000`.

---

## 🤖 AI Chat — Setup (Optional)

The AI Chat panel is powered by the **NVIDIA NIM API** (running the Qwen model). To enable real responses:

1. Get your API key from [build.nvidia.com](https://build.nvidia.com)
2. Add your key to your `.env` file: `NVIDIA_API_KEY=your_key_here`

> **Without a key**, the chat will fallback to smart local responses for balance, spending, and general queries based on your account data.

---

## 📸 Dashboard Views

```
📊 Dashboard     →  Stat cards, income/expense bar chart, recent transactions, 
                    donut chart, budget status, AI insight card
💳 Transactions  →  Full filterable/searchable transaction table
📈 Analytics     →  Cash flow line chart, category bar chart, savings growth, heatmap
🎯 Budgets       →  6-category budget cards with visual spend percentage
🏆 Goals         →  Savings goal cards with progress bars & timelines
──────────────────────────────────────────────────────────────────
📈 Investments   →  Portfolio growth chart, asset allocation, quick actions  [NEW]
🏦 Loans & EMI   →  Active loans with repayment progress & EMI countdown     [NEW]
💎 Net Worth     →  Total position, balance sheet, wealth growth chart        [NEW]
──────────────────────────────────────────────────────────────────
🤖 AI Insights   →  4 smart insight cards (alert · win · tip · trend)
📄 Reports       →  Export Monthly / Annual / Tax / Budget / Goals PDF & CSV
👤 Profile       →  Personal info, security settings, plan details
⚙️ Settings      →  Notifications, preferences, data & privacy, subscription
```

---

## 🔐 Privacy & Security

SmartSpend uses a secure **Python Flask + MySQL backend** to safely store your data. 

Fully aligned with standard security practices:
- 🔒 **JWT Authentication** to secure your session and endpoints
- 🔑 **Password Hashing** for all user accounts
- 🇮🇳 **DPDP Act 2023** (India's Data Protection Law) ready
- 🇪🇺 **GDPR** (General Data Protection Regulation) ready

---

## 📜 Changelog

| Version | Changes |
|---|---|
| **v3.0** | + Google Sign-In · + Onboarding Setup Wizard · + Billing & Subscription Plans · + Live AI Chat with Memory · + Real-time Smart Notifications |
| **v2.0** | + Investments, Loans & EMI, Net Worth views · + AI Chat Assistant · + Claymorphism redesign |
| **v1.0** | Initial dashboard with transactions, analytics, budgets, goals, AI insights |

---

## 👨‍💻 Author

Built with 💚 in India

**SmartSpend Technologies Pvt. Ltd.**

---

<div align="center">

© 2026 SmartSpend Technologies · All rights reserved.

[Privacy Policy](privacy.html) · [Terms of Service](terms.html) · [Security](security.html) · [Contact](contact.html)

</div>
