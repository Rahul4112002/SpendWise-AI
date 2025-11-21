# 🎉 PennyWise AI - Complete Installation & Setup Guide

## InTech Problem Statement 1 Implementation
**Autonomous Financial Coaching Agent for Gig Workers & Everyday Citizens**

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features Implemented](#features-implemented)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

PennyWise AI is a comprehensive web-based autonomous financial coaching platform that:
- ✅ Automatically tracks expenses from SMS and bank statements
- ✅ Provides AI-powered spending analysis
- ✅ Detects anomalies and unusual spending patterns
- ✅ Identifies recurring subscriptions
- ✅ Generates personalized budget recommendations
- ✅ Adapts to income variability (perfect for gig workers)
- ✅ Offers interactive AI financial coaching

---

## 🚀 Features Implemented

### Backend (FastAPI + Python)
✅ **Authentication System**
- JWT-based secure authentication
- User registration & login
- Password hashing with bcrypt

✅ **SMS Transaction Parser**
- Support for 40+ Indian banks
- Automatic amount, merchant, and category extraction
- Recurring payment detection

✅ **Bank Statement Processing**
- PDF parsing with password support
- Automatic transaction extraction
- Bank name and account detection

✅ **AI Financial Coach** (LangChain + Groq)
- Spending pattern analysis
- Anomaly detection
- Subscription identification
- Budget recommendations
- Interactive chat interface
- Income variability adaptation

✅ **Analytics Engine**
- Category-wise spending breakdown
- Monthly trend analysis
- Top merchants tracking
- Daily spending patterns

✅ **Complete API Endpoints**
- `/api/v1/auth` - Authentication
- `/api/v1/transactions` - Transaction management
- `/api/v1/bank-statements` - PDF upload & processing
- `/api/v1/analytics` - Spending analytics
- `/api/v1/ai` - AI coaching & chat
- `/api/v1/budgets` - Budget management
- `/api/v1/categories` - Category management

### Frontend (React)
✅ **Dashboard**
- Financial overview
- Top spending categories
- Monthly trends
- AI insights display

✅ **AI Chat Interface**
- Interactive financial coaching
- Quick question suggestions
- Real-time responses

✅ **Authentication UI**
- Login & Registration forms
- Protected routes

✅ **Responsive Design**
- Mobile-friendly interface
- Modern UI with gradients

---

## 📦 Prerequisites

### Required Software
1. **Python 3.12+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Node.js 16+**
   - Download: https://nodejs.org/
   - Verify: `node --version`

3. **PostgreSQL 14+**
   - Download: https://www.postgresql.org/download/
   - OR use SQLite for development (included)

4. **Git** (optional but recommended)
   - Download: https://git-scm.com/downloads

### API Keys Required
- **Groq API Key** (FREE): https://console.groq.com/keys
  - Sign up for free
  - Create an API key
  - Copy the key for later use

---

## ⚡ Quick Start

### Option 1: Automated Setup (Windows)

1. **Clone or download this project**
```cmd
cd c:\Users\RAHUL\OneDrive\Desktop\pennywise-web
```

2. **Run the setup script**
```cmd
quick-start.bat
```

3. **Configure environment**
- Edit `backend\.env` and add your GROQ_API_KEY
- Optionally update DATABASE_URL

4. **Start the application**
```cmd
# Terminal 1 - Backend
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

### Option 2: Manual Setup

Follow the [Detailed Setup](#detailed-setup) section below.

---

## 🔧 Detailed Setup

### Step 1: Backend Setup

```cmd
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

1. Copy the example env file:
```cmd
copy .env.example .env
```

2. Edit `backend\.env` with your values:
```env
# Database (use one of these)
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/pennywise
# OR for quick start with SQLite:
# DATABASE_URL=sqlite:///./pennywise.db

# Secret Key (generate a secure one)
SECRET_KEY=your-super-secret-key-change-this

# Groq API Key (get from https://console.groq.com)
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=mixtral-8x7b-32768

# Other settings
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### Step 3: Initialize Database

**Option A: PostgreSQL**
```cmd
# Create database
createdb pennywise

# OR using psql:
psql -U postgres
CREATE DATABASE pennywise;
\q
```

**Option B: SQLite (Easiest for development)**
- Just set `DATABASE_URL=sqlite:///./pennywise.db` in `.env`
- Database file will be created automatically

### Step 4: Frontend Setup

```cmd
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env
```

Edit `frontend\.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

---

## 🎮 Running the Application

### Start Backend Server

```cmd
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend will be running at: http://localhost:8000
✅ API Documentation: http://localhost:8000/docs

### Start Frontend Development Server

```cmd
cd frontend
npm start
```

✅ Frontend will be running at: http://localhost:3000

### Access the Application

1. Open browser: http://localhost:3000
2. Register a new account
3. Login and start using PennyWise AI!

---

## 📚 API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

#### Transactions
- `POST /api/v1/transactions` - Create transaction
- `GET /api/v1/transactions` - Get all transactions
- `POST /api/v1/transactions/sms-batch` - Process SMS batch

#### Analytics
- `GET /api/v1/analytics/summary` - Get spending summary
- `GET /api/v1/analytics/spending-by-category` - Category breakdown
- `GET /api/v1/analytics/income-vs-expenses` - Monthly comparison

#### AI Coach
- `POST /api/v1/ai/chat` - Chat with AI
- `POST /api/v1/ai/analyze-spending` - Get AI analysis
- `GET /api/v1/ai/insights` - Get AI insights
- `POST /api/v1/ai/detect-anomalies` - Detect unusual spending
- `GET /api/v1/ai/subscriptions` - Identify subscriptions

#### Budgets
- `POST /api/v1/budgets` - Create budget
- `GET /api/v1/budgets` - Get all budgets
- `PUT /api/v1/budgets/{id}` - Update budget

#### Categories
- `GET /api/v1/categories` - Get all categories
- `POST /api/v1/categories/init-default` - Initialize default categories

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: "Module not found" errors**
```cmd
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Database connection error**
- For PostgreSQL: Verify service is running
  ```cmd
  # Windows: Check Services
  # Linux/Mac: sudo service postgresql status
  ```
- For SQLite: Ensure write permissions in project directory

**Issue: GROQ_API_KEY not working**
- Verify key is correct in `.env` file
- Check if you have API credits at https://console.groq.com
- Try a different model: `llama-3.1-70b-versatile`

### Frontend Issues

**Issue: "Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check `frontend\.env` has correct API URL
- Verify CORS settings in backend `.env`

**Issue: npm install fails**
```cmd
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### General Tips

1. **Check terminal output** for specific error messages
2. **Verify all environment variables** are set correctly
3. **Ensure all required services are running**:
   - Backend server (port 8000)
   - Frontend server (port 3000)
   - Database (PostgreSQL or SQLite)

---

## 📖 Usage Guide

### 1. Initial Setup After First Login

1. **Initialize Categories**
   - Visit Categories page
   - Click "Initialize Default Categories"

2. **Add First Transaction**
   - Click "Add Transaction" on dashboard
   - Or upload a bank statement PDF

3. **Chat with AI**
   - Go to AI Chat
   - Ask questions like "How much did I spend on food?"

### 2. Understanding the Dashboard

- **Summary Cards**: Total income, expenses, savings, transactions
- **Top Categories**: Where your money goes
- **Monthly Trends**: Income vs expenses over time
- **AI Insights**: Proactive recommendations

### 3. Using AI Features

**Spending Analysis**:
- Automatic after adding transactions
- View on dashboard

**Anomaly Detection**:
- Identifies unusual spending
- Alerts on high-priority issues

**Budget Recommendations**:
- Adapts to your income variability
- Personalized category limits

---

## 🎓 For Developers

### Project Structure
```
pennywise-web/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── core/                # Config & security
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API client
│   │   └── App.js
│   ├── package.json
│   └── .env
└── README.md
```

### Running Tests
```cmd
# Backend tests
cd backend
pytest

# Frontend tests  
cd frontend
npm test
```

---

## 🤝 Contributing

This is a demonstration project for InTech Problem Statement 1.

---

## 📄 License

MIT License - Feel free to use for educational purposes

---

## 🙋 Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Check API documentation at `/docs`

---

## 🎉 Next Steps

After successful setup:
1. ✅ Register an account
2. ✅ Add some transactions or upload a statement
3. ✅ Explore the AI chat
4. ✅ Create budgets
5. ✅ View analytics

**Congratulations! You now have a fully functional autonomous financial coaching platform!** 🚀
