# 🚀 PennyWise AI - Quick Reference Guide

## ⚡ Quick Start (3 Commands)

```cmd
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Install frontend dependencies
cd ../frontend
npm install

# 3. Add GROQ API key to backend\.env
# Then run:
START.bat
```

---

## 🔑 Get Your Free Groq API Key

1. Visit: https://console.groq.com
2. Sign up (free)
3. Go to "API Keys"
4. Create new key
5. Copy and paste into `backend\.env`:
   ```
   GROQ_API_KEY=your-key-here
   ```

---

## 🎯 First Time Setup

### 1. Configure Backend
Edit `backend\.env`:
```env
DATABASE_URL=sqlite:///./pennywise.db
GROQ_API_KEY=gsk_your_groq_api_key_here
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
DEBUG=True
```

### 2. Configure Frontend
Edit `frontend\.env`:
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### 3. Run the Application
```cmd
START.bat
```

Or manually:
```cmd
# Terminal 1 - Backend
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## 📱 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🎓 First Steps After Login

1. **Initialize Categories**
   - Go to Categories page
   - Click "Initialize Default Categories"

2. **Add a Transaction**
   - Click "Add Transaction"
   - Or upload a bank statement

3. **Chat with AI**
   - Go to AI Chat
   - Ask: "Analyze my spending"

4. **Create a Budget**
   - Go to Budgets
   - Click "Generate AI Budget"

---

## 🔧 Common Commands

### Backend

```cmd
# Activate virtual environment
cd backend
.venv\Scripts\activate

# Run server
uvicorn app.main:app --reload

# Install new package
pip install package-name
pip freeze > requirements.txt

# Database (if using PostgreSQL)
createdb pennywise
```

### Frontend

```cmd
# Start development server
npm start

# Build for production
npm run build

# Install new package
npm install package-name
```

---

## 📊 API Endpoints Reference

### Authentication
```
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### Transactions
```
POST /api/v1/transactions
GET  /api/v1/transactions
POST /api/v1/transactions/sms-batch
```

### Analytics
```
GET /api/v1/analytics/summary?days=30
GET /api/v1/analytics/spending-by-category
GET /api/v1/analytics/income-vs-expenses
GET /api/v1/analytics/top-merchants
```

### AI Coach
```
POST /api/v1/ai/chat
POST /api/v1/ai/analyze-spending
GET  /api/v1/ai/insights
POST /api/v1/ai/detect-anomalies
GET  /api/v1/ai/subscriptions
```

### Budgets
```
POST /api/v1/budgets
GET  /api/v1/budgets
PUT  /api/v1/budgets/{id}
```

### Categories
```
GET  /api/v1/categories
POST /api/v1/categories/init-default
```

---

## 🐛 Quick Troubleshooting

### Backend Issues

**Problem**: Module not found
```cmd
cd backend
pip install -r requirements.txt --force-reinstall
```

**Problem**: Database error
```cmd
# For SQLite - just use this in .env:
DATABASE_URL=sqlite:///./pennywise.db
```

**Problem**: GROQ API not working
- Check key is correct in `.env`
- Visit https://console.groq.com to verify
- Try different model: `llama-3.1-70b-versatile`

### Frontend Issues

**Problem**: Cannot connect to backend
- Ensure backend is running: http://localhost:8000
- Check `frontend\.env` has: `REACT_APP_API_URL=http://localhost:8000/api/v1`

**Problem**: npm install fails
```cmd
npm cache clean --force
del package-lock.json
npm install
```

---

## 📝 Sample API Request (cURL)

### Register User
```cmd
curl -X POST http://localhost:8000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\",\"name\":\"Test User\"}"
```

### Login
```cmd
curl -X POST http://localhost:8000/api/v1/auth/login ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=test@example.com&password=password123"
```

### Chat with AI
```cmd
curl -X POST http://localhost:8000/api/v1/ai/chat ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"How much did I spend on food?\"}"
```

---

## 🎯 Key Files to Know

### Backend
- `backend/app/main.py` - FastAPI application
- `backend/app/core/config.py` - Settings
- `backend/app/services/ai_coach.py` - AI financial coach
- `backend/requirements.txt` - Dependencies
- `backend/.env` - Configuration

### Frontend
- `frontend/src/App.js` - Main app component
- `frontend/src/components/Dashboard/Dashboard.js` - Main dashboard
- `frontend/src/components/AI/AIChat.js` - AI chat interface
- `frontend/package.json` - Dependencies
- `frontend/.env` - Configuration

---

## 💡 Tips & Tricks

1. **Test API in Browser**
   - Visit http://localhost:8000/docs
   - Try out endpoints interactively

2. **View Backend Logs**
   - Check terminal running uvicorn
   - Errors will show there

3. **Debug Frontend**
   - Open browser DevTools (F12)
   - Check Console tab for errors
   - Check Network tab for API calls

4. **Reset Database**
   - For SQLite: Delete `pennywise.db` file
   - Restart backend - new DB created

5. **Change AI Model**
   - Edit `backend/.env`
   - Try: `mixtral-8x7b-32768`, `llama-3.1-70b-versatile`

---

## 📚 Documentation

- **README.md** - Project overview
- **INSTALLATION.md** - Detailed setup
- **COMPLETE_PROJECT_SUMMARY.md** - All features
- **API Docs** - http://localhost:8000/docs

---

## ✅ Checklist for New Setup

- [ ] Python 3.12+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] GROQ_API_KEY added to backend/.env
- [ ] Database configured (SQLite recommended for start)
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can register/login
- [ ] Can see API docs at /docs

---

## 🎉 You're Ready!

Once all checklist items are done:
1. Register an account
2. Add some transactions
3. Chat with AI
4. Explore analytics

**Need Help?** See INSTALLATION.md for detailed guides!

---

**Quick Links**:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Groq Console: https://console.groq.com
