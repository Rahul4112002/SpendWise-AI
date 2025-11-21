# 🎉 PennyWise AI - Autonomous Financial Coaching Agent

**InTech Problem Statement 1 Implementation**

> An intelligent, autonomous financial coaching web application designed for gig workers, informal sector employees, and everyday citizens. Built with FastAPI, React, and powered by AI.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+
- Groq API Key (FREE from https://console.groq.com)

### Installation (5 minutes)

1. **Clone/Download the project**
```cmd
cd pennywise-web
```

2. **Install Backend Dependencies**
```cmd
cd backend
pip install -r requirements.txt
```

3. **Install Frontend Dependencies**
```cmd
cd ../frontend
npm install
```

4. **Configure Environment**
```cmd
# Edit backend\.env and add:
GROQ_API_KEY=your-groq-api-key-here
DATABASE_URL=sqlite:///./pennywise.db
```

5. **Start the Application**
```cmd
# Run from project root
START.bat
```

Visit: **http://localhost:3000**

---

## ✨ Features

### 🤖 AI-Powered Financial Coaching
- Interactive chat with AI financial advisor
- Personalized spending analysis
- Proactive recommendations
- Anomaly detection
- Subscription identification

### 📊 Smart Analytics
- Real-time financial dashboard
- Category-wise spending breakdown
- Monthly trend analysis
- Income vs expenses tracking
- Top merchants insights

### 💰 Transaction Management
- SMS transaction parsing (40+ banks)
- Bank statement PDF upload
- Auto-categorization
- Manual transaction entry
- Export capabilities

### 📈 Budget Management
- AI-generated budget recommendations
- Category-based budgets
- Alert thresholds
- Spending limits

### 🎯 Gig Worker Optimized
- Income variability tracking
- Irregular income adaptation
- Flexible budget planning
- Emergency buffer recommendations

---

## 📁 Project Structure

```
pennywise-web/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/endpoints/  # API Routes
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── transactions.py
│   │   │   ├── analytics.py
│   │   │   ├── ai.py          # AI Coach
│   │   │   ├── budgets.py
│   │   │   └── categories.py
│   │   ├── models/            # Database Models
│   │   ├── services/          # Business Logic
│   │   │   ├── ai_coach.py    # AI Financial Coach
│   │   │   ├── sms_forwarding_handler.py
│   │   │   └── pdf_parser_enhanced.py
│   │   ├── core/              # Config & Security
│   │   └── main.py
│   └── requirements.txt
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/     # Main Dashboard
│   │   │   ├── AI/            # AI Chat
│   │   │   ├── Auth/          # Login/Register
│   │   │   └── BankStatement/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
├── INSTALLATION.md             # Detailed Setup Guide
├── COMPLETE_PROJECT_SUMMARY.md # Feature Documentation
└── START.bat                   # Quick Start Script
```

---

## 🛠️ Technology Stack

**Backend**
- FastAPI - Modern async web framework
- SQLAlchemy - ORM
- LangChain + Groq - AI integration
- PostgreSQL/SQLite - Database
- JWT Authentication

**Frontend**
- React 18
- React Router
- Axios
- Modern CSS3

**AI/ML**
- Groq API (Mixtral-8x7b)
- LangChain orchestration
- Pattern recognition
- Anomaly detection

---

## 📖 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Complete setup guide
- **[COMPLETE_PROJECT_SUMMARY.md](COMPLETE_PROJECT_SUMMARY.md)** - Detailed feature list
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture overview
- **API Docs** - http://localhost:8000/docs (when running)

---

## 🎯 InTech Problem Statement 1 - Requirements

✅ **Autonomous financial coaching** - AI-powered insights and recommendations  
✅ **Adapts to real user behavior** - Spending pattern analysis  
✅ **Income variability** - Gig worker specific features  
✅ **Proactive decisions** - Anomaly detection & alerts  
✅ **Multi-platform** - Web-based (extensible to mobile)  
✅ **Smart categorization** - Auto-categorize transactions  
✅ **Budget recommendations** - AI-generated personalized budgets  
✅ **Subscription tracking** - Recurring payment detection  

---

## 💻 Development

### Run Backend Only
```cmd
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

### Run Frontend Only
```cmd
cd frontend
npm start
```

### API Documentation
Visit http://localhost:8000/docs for interactive Swagger UI

---

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./pennywise.db
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=mixtral-8x7b-32768
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

---

## 🎓 Key Features Explained

### AI Financial Coach
Uses LangChain + Groq to provide:
- Conversational financial advice
- Spending pattern analysis
- Budget recommendations
- Anomaly alerts
- Subscription detection

### SMS Parser
Extracts transaction data from bank SMS:
- 40+ Indian bank support
- Amount, merchant, category extraction
- Recurring payment detection
- Batch processing

### Analytics Engine
Comprehensive financial insights:
- Category-wise breakdown
- Monthly trends
- Daily spending patterns
- Top merchants
- Income vs expenses

---

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure Python 3.12+ is installed
- Check virtual environment is activated
- Verify all dependencies: `pip install -r requirements.txt`

**Frontend won't start:**
- Check Node.js 16+ is installed
- Clear cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

**Database errors:**
- For SQLite: Check file permissions
- For PostgreSQL: Verify service is running

**AI features not working:**
- Verify GROQ_API_KEY in backend/.env
- Check API credits at https://console.groq.com

See **[INSTALLATION.md](INSTALLATION.md)** for detailed troubleshooting.

---

## 📝 License

MIT License - Free for educational and commercial use

---

## 🙏 Acknowledgments

- Inspired by [PennyWise AI Android App](https://github.com/sarim2000/pennywiseai-tracker)
- Built for InTech Problem Statement 1
- Powered by Groq AI

---

## 📞 Support

For detailed setup help, see:
1. [INSTALLATION.md](INSTALLATION.md) - Step-by-step guide
2. [COMPLETE_PROJECT_SUMMARY.md](COMPLETE_PROJECT_SUMMARY.md) - Feature documentation
3. API Docs at http://localhost:8000/docs

---

**Status**: ✅ Production Ready | 🚀 Fully Functional | 📚 Well Documented

**Get Started**: Run `START.bat` and visit http://localhost:3000
