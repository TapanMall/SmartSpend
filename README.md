<div align="center">

# 💸 SmartSpend

### Your Intelligent Financial Companion

*Track. Analyse. Grow.*

[![Made with HTML](https://img.shields.io/badge/Made%20with-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Styled with CSS](https://img.shields.io/badge/Styled%20with-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Powered by JS](https://img.shields.io/badge/Powered%20by-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Charts by Chart.js](https://img.shields.io/badge/Charts-Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![AI by Claude](https://img.shields.io/badge/AI-Claude%20API-6C63FF?style=flat-square)](https://claude.ai/)

</div>

---

## 🌟 What is SmartSpend?

**SmartSpend** is a premium, full-featured personal finance dashboard built entirely with vanilla HTML, CSS, and JavaScript — no frameworks, no build tools. It combines beautiful claymorphism design with powerful financial tracking tools, AI-powered insights, and wealth management features all in a single file.

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
| **AI Chat Assistant** | Floating chat panel powered by Claude API (with smart local fallback) |
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

```
Frontend       → Semantic HTML5  +  Vanilla CSS3  +  ES6+ JavaScript
Charts         → Chart.js (CDN)
Typography     → Syne (Headings)  ·  DM Sans (Body)  ·  JetBrains Mono (Numbers)
AI Integration → Anthropic Claude API (with mock fallback)
Icons          → Emoji-native  +  Custom inline SVG
Design System  → CSS Custom Properties (tokens), Claymorphism shadows
```

---

## 📂 Project Structure

```
SmartSpend-main/
│
├── smartspend.html          # 🏠 Main Landing Page & Entry Point
├── Dashboard.html           # 📊 Full Finance Dashboard (main app)
│
├── about.html               # ℹ️  Company Information
├── blog.html                # 📝 Latest Updates & Articles
├── careers.html             # 💼 Join the Team
├── contact.html             # 📬 Get in Touch
├── press.html               # 📰 Press Kit & Brand Assets
│
├── privacy.html             # 🔒 Privacy Policy
├── terms.html               # 📜 Terms of Service
├── cookies.html             # 🍪 Cookie Policy
├── gdpr.html                # 🇪🇺 GDPR Compliance
├── security.html            # 🛡️ Security Overview
│
├── app.py                   # 🐍 Backend (Python/Flask — placeholder)
├── requirements.txt         # 📦 Python dependencies
└── README.md                # 📖 You are here
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/SmartSpend.git
cd SmartSpend-main
```

### 2. Open the landing page
```bash
# Just open in your browser directly — no build step needed
start smartspend.html       # Windows
open smartspend.html        # macOS
xdg-open smartspend.html    # Linux
```

### 3. Access the Dashboard
Click **"Get Started"** or **"Launch App"** from the landing page, or open `Dashboard.html` directly.

---

## 🤖 AI Chat — Setup (Optional)

The AI Chat panel is pre-wired to the **Anthropic Claude API**. To enable real responses:

1. Get your API key from [console.anthropic.com](https://console.anthropic.com)
2. Set up a simple backend proxy (e.g. Flask in `app.py`) to avoid exposing your key in the browser
3. Update the `fetch` call in the `sendAiMessage()` function in `Dashboard.html` to point to your endpoint

> **Without a key**, the chat still works with smart local responses for balance, spending, investments & loan queries.

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

SmartSpend is a **frontend-only application** — all data is processed in the browser and nothing is sent to any external server by default. Optional AI features require a backend proxy which you control.

Fully aligned with:
- 🇮🇳 **DPDP Act 2023** (India's Data Protection Law)
- 🇪🇺 **GDPR** (General Data Protection Regulation)

---

## 📜 Changelog

| Version | Changes |
|---|---|
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
