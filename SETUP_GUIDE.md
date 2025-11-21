# 🚀 PennyWise AI - Setup & Installation Guide

## ✅ What's Been Created

Your PennyWise AI project now includes:

### Backend (FastAPI + Python)
✅ **Core Configuration**
- Config management with Pydantic Settings
- JWT authentication & security
- CORS middleware
- Environment variable support

✅ **Database Models**
- User (with income variability tracking)
- Transaction (with SMS metadata & categorization)
- BankStatement (PDF upload support)
- Category, Budget, AIInsight, SpendingPattern

✅ **Services**
- **SMS Parser** - Extracts transactions from bank SMS (40+ banks)
- **PDF Parser** - Processes bank statements with password support
- **AI Coach** - LangChain + Groq powered financial advisor
  - Spending pattern analysis
  - Anomaly detection
  - Subscription identification
  - Personalized budget recommendations
  - Interactive chat

✅ **API Endpoints**
- Authentication (register, login)
- Transactions management
- Bank statement upload
- User profile

### Frontend (React)
✅ **Core Setup**
- React Router navigation
- Auth Context & hooks
- API service layer
- Responsive styling
- Login/Register components

## 📋 Next Steps to Complete Setup

### Step 1: Install Backend Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL Database

```bash
# Install PostgreSQL if not already installed
# Windows: Download from https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Create database
createdb pennywise

# Or using psql:
psql -U postgres
CREATE DATABASE pennywise;
\q
```

### Step 3: Configure Environment Variables

```bash
cd backend

# Copy the example file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Edit .env and add:
```

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/pennywise
SECRET_KEY=generate-a-secure-random-key-at-least-32-characters-long
GROQ_API_KEY=your-groq-api-key-from-console.groq.com
GROQ_MODEL=mixtral-8x7b-32768
DEBUG=True
```

**Get Groq API Key:**
1. Visit https://console.groq.com
2. Sign up/Login
3. Go to API Keys section
4. Create new API key
5. Copy and paste into .env

### Step 4: Run Backend

```bash
cd backend

# Make sure virtual environment is activated
# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: http://localhost:8000
API Docs: http://localhost:8000/docs

### Step 5: Install Frontend Dependencies

```bash
cd frontend

# Install Node packages
npm install
```

### Step 6: Configure Frontend

```bash
cd frontend

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# .env content:
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Step 7: Run Frontend

```bash
cd frontend

# Start development server
npm start
```

Frontend will be running at: http://localhost:3000

## 🎯 Testing the Application

### 1. Register a New User

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123",
    "full_name": "Test User",
    "user_type": "gig_worker",
    "average_monthly_income": 50000,
    "income_variability": "high"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=securepassword123"
```

### 3. Test SMS Parser

Create a Python script to test:

```python
from app.services.sms_forwarding_handler import SMSParser

parser = SMSParser()

sms_text = "Your A/C XX1234 debited by Rs.1,500.00 at ZOMATO ONLINE on 21-Nov-24"
result = parser.parse_sms(sms_text, "HDFCBK")

print(result)
# Output: Transaction details with amount, merchant, category, etc.
```

## 🔧 Additional Features to Implement

### Priority 1 - Complete API Endpoints

Create these endpoint files:

1. **`backend/app/api/v1/endpoints/ai.py`** - AI insights & chat
2. **`backend/app/api/v1/endpoints/analytics.py`** - Spending analytics
3. **`backend/app/api/v1/endpoints/budgets.py`** - Budget management

### Priority 2 - Frontend Components

Complete these components:

1. **Dashboard/ExpenseTracker.js** - Main dashboard
2. **Dashboard/Reports.js** - Analytics & charts
3. **Dashboard/Notifications.js** - AI alerts
4. **BankStatement/UploadStatement.js** - PDF upload
5. **Common/Header.js & Footer.js** - Navigation

### Priority 3 - AI Integration

1. Test Groq API connectivity
2. Implement spending analysis workflow
3. Add chat interface
4. Create notification system

## 📚 Project Structure

```
pennywise-web/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/  # API routes
│   │   ├── core/              # Config & security
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   ├── main.py           # FastAPI app
│   │   └── database.py       # DB connection
│   ├── uploads/              # User uploads
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── contexts/         # React contexts
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # API calls
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env
└── README.md
```

## ❓ Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Database connection error

```bash
# Check PostgreSQL is running
# Windows: Check Services
# Mac: brew services list
# Linux: sudo systemctl status postgresql

# Test connection
psql -U postgres -d pennywise
```

### Frontend build errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS errors

- Make sure backend CORS_ORIGINS in .env includes frontend URL
- Check frontend is making requests to correct API URL

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **LangChain**: https://python.langchain.com
- **Groq API**: https://console.groq.com/docs

## 📞 Need Help?

- Check API docs: http://localhost:8000/docs
- Review backend logs in terminal
- Check browser console for frontend errors

---

**You're all set! Start building your autonomous financial coach! 🎉**
