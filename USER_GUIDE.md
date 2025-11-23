# 📱 SpendWise AI - Complete User Guide

## 🚀 Step-by-Step Guide: How to Use the Project

---

## **Step 1: Starting the Application**

### **A. Start Backend Server**
```bash
# Open Terminal 1
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
✅ Backend will run on: `http://localhost:8000`

### **B. Start Frontend Server**
```bash
# Open Terminal 2
cd frontend
npm start
```
✅ Frontend will open automatically on: `http://localhost:3001`

---

## **Step 2: First Time User - Registration**

### **1. Open Registration Page**
- Browser mein `http://localhost:3001` open karo
- Automatically **Login page** dikhai dega
- Neeche **"Don't have an account? Register"** link par click karo

### **2. Fill Registration Form**
**Required Fields:**
- **Full Name**: `Rahul Chauhan`
- **Email**: `rahul@example.com`
- **Phone Number**: `+918828489397` (optional)
- **Password**: `YourPassword123`
- **Confirm Password**: `YourPassword123` (same as password)

### **3. Click "Register" Button**
- ✅ Success message: **"Registration successful! Redirecting to login..."**
- Automatically 2 seconds mein login page par redirect ho jayega

---

## **Step 3: Login to Your Account**

### **1. Enter Login Credentials**
- **Email**: `rahul@example.com`
- **Password**: `YourPassword123`

### **2. Click "Login" Button**
- ✅ JWT token generate hoga
- ✅ Automatically **Dashboard** par redirect ho jayega

---

## **Step 4: Dashboard - Your Financial Overview**

### **Dashboard mein kya dikhega:**

#### **A. Summary Cards (Top Section)**
```
💰 Total Income        💸 Total Expenses
₹50,000                ₹35,000

🏦 Net Savings         📊 Transactions
₹15,000 (30% rate)     45 transactions
```

#### **B. Top Spending Categories**
- Food & Dining: ₹8,500 (24%)
- Transport: ₹6,200 (18%)
- Shopping: ₹5,800 (16%)
- Bills: ₹4,500 (13%)
- Progress bars show percentage

#### **C. AI Insights Section**
- 🤖 AI-generated recommendations
- Priority badges (High/Medium/Low)
- Spending alerts
- Saving tips

#### **D. Quick Actions (Bottom)**
4 buttons dikhenge:
1. ➕ Add Transaction
2. 📄 Upload Statement
3. 💬 Chat with AI
4. 📊 Manage Budgets

---

## **Step 5: Upload Bank Statement (PDF)**

### **Option 1: From Dashboard**
- Click **"Upload Statement"** button

### **Option 2: From Header Menu**
- Click **"Upload"** in top navigation

### **Steps:**
1. **Select PDF File**
   - Click "Choose File" button
   - Select your bank statement PDF (e.g., `hdfc_statement.pdf`)
   - ✅ File name dikhai dega: "Selected: hdfc_statement.pdf"

2. **Click "Upload & Process"**
   - Backend automatically:
     - PDF extract karega
     - Transactions parse karega
     - Categories assign karega
   
3. **Success Message**
   ```
   ✅ Upload successful! 25 transactions extracted.
   ```

4. **View Extracted Transactions**
   - Go to **"Transactions"** page
   - Sare extracted transactions list mein dikhenge

---

## **Step 6: View Transaction History**

### **Navigate to Transactions Page**
- Header menu mein **"Transactions"** click karo

### **What You'll See:**
```
Transaction History
┌─────────────────────────────────────────────┐
│ Amazon Shopping                             │
│ Shopping                                    │
│ 15 Nov 2024                          -₹2,499│
├─────────────────────────────────────────────┤
│ Swiggy Food Delivery                        │
│ Food                                        │
│ 14 Nov 2024                            -₹450│
├─────────────────────────────────────────────┤
│ Salary Credit                               │
│ Income                                      │
│ 01 Nov 2024                         +₹50,000│
└─────────────────────────────────────────────┘
```

**Features:**
- 🔴 Red for Debit (-₹)
- 🟢 Green for Credit (+₹)
- Category tags
- Date and merchant name
- Scrollable list

---

## **Step 7: Chat with AI Financial Coach**

### **Open AI Chat**
- Header menu mein **"AI Chat"** click karo
- Ya Dashboard se **"Chat with AI"** button

### **Chat Interface:**
```
🤖 AI Financial Coach
┌─────────────────────────────────────────┐
│ Hi! I'm your AI financial coach.        │
│ Ask me anything about your finances!    │
└─────────────────────────────────────────┘

Quick Questions:
[Analyze my spending] [Budget tips] [Save money]
```

### **Example Conversations:**

**User:** "Analyze my spending this month"
```
🤖 AI: Based on your transactions:
- You spent ₹8,500 on food (24% of expenses)
- Transport costs are ₹6,200 (18%)
- Recommendation: Try cooking at home 2-3 days/week 
  to save ₹2,000-3,000 monthly
```

**User:** "Should I create a budget?"
```
🤖 AI: Yes! Based on your ₹50,000 income, I suggest:
- Food: ₹8,000 (16%)
- Transport: ₹6,000 (12%)
- Bills: ₹5,000 (10%)
- Savings: ₹15,000 (30%)
- Emergency Fund: ₹5,000 (10%)
```

**User:** "Any unusual transactions?"
```
🤖 AI: I detected 1 anomaly:
- Amazon purchase of ₹12,499 on Nov 18
  This is 4.2x your average shopping expense
  Confidence: 92%
```

---

## **Step 8: View Financial Reports**

### **Navigate to Reports**
- Click **"Reports"** in header menu

### **Available Reports:**

#### **1. Monthly Report**
- Click **"Generate Report"** button
- Shows month-wise breakdown
- Income vs Expenses comparison

#### **2. Spending Trends**
- Click **"View Trends"** button
- Category-wise spending over time
- Identifies patterns

#### **3. Budget Analysis**
- Click **"View Analysis"** button
- Budget vs Actual comparison
- Over/Under spending alerts

#### **4. Export Data**
- Click **"Export"** button
- Download transactions as CSV/PDF

---

## **Step 9: AI-Powered Features (Automatic)**

### **A. Anomaly Detection**
**Kya hota hai:**
- AI automatically unusual transactions detect karta hai
- 3x se zyada spending = Anomaly

**Example:**
```
⚠️ Unusual Transaction Detected
₹15,000 spent at Croma Electronics
This is 5x your average electronics spending
Date: Nov 20, 2024
```

### **B. Subscription Detection**
**Kya hota hai:**
- Recurring payments automatically identify hote hain

**Example:**
```
🔄 Subscriptions Found:
1. Netflix - ₹649/month (Last: Nov 15)
2. Amazon Prime - ₹1,499/year (Next: Dec 10)
3. Spotify - ₹119/month (Last: Nov 18)

Total Monthly: ₹768
```

### **C. Budget Recommendations**
**Kya hota hai:**
- AI apke income ke basis par budget suggest karta hai

**Example:**
```
💡 Smart Budget Suggestion
Based on ₹50,000 monthly income:

Essential (50%): ₹25,000
- Rent: ₹12,000
- Food: ₹8,000
- Bills: ₹5,000

Lifestyle (30%): ₹15,000
- Shopping: ₹6,000
- Entertainment: ₹4,000
- Transport: ₹5,000

Savings (20%): ₹10,000
```

---

## **Step 10: Email Integration (Future Feature)**

### **Connect Your Gmail**
1. Go to **Settings** (coming soon)
2. Click **"Connect Gmail"**
3. Allow permissions
4. AI will automatically:
   - Fetch transaction emails
   - Parse bank notifications
   - Extract amounts and merchants
   - Add to transaction history

### **Supported Email Types:**
- ✅ Bank transaction alerts
- ✅ Credit card statements
- ✅ UPI payment receipts
- ✅ Online purchase confirmations

---

## **Step 11: Managing Your Profile**

### **Update Profile**
- Click your **name** in header (top right)
- Select **"Profile"** from dropdown

### **Editable Fields:**
- Full Name
- Phone Number
- User Type (Gig Worker/Regular Employee)
- Average Monthly Income
- Income Variability (Low/Medium/High)
- Preferred Currency (INR/USD)
- Timezone

---

## **Step 12: Logout**

### **Sign Out**
- Click **"Logout"** button in header
- JWT token delete ho jayega
- Login page par redirect ho jayega

---

## 🎯 **Complete User Journey Example**

### **Day 1: Setup**
1. ✅ Register account
2. ✅ Login
3. ✅ Upload last 3 months bank statements
4. ✅ AI automatically analyzes 150+ transactions

### **Day 2: Insights**
1. ✅ Check Dashboard - See income/expense summary
2. ✅ Chat with AI - Ask "Where am I overspending?"
3. ✅ AI suggests: "Food spending is 35%, reduce to 20%"
4. ✅ Create budget for Food: ₹8,000/month

### **Day 3: Monitoring**
1. ✅ AI detects subscription: Netflix ₹649/month
2. ✅ AI alerts: "Unusual ₹15,000 electronics purchase"
3. ✅ View Reports - Monthly trend shows improvement

### **Day 4: Ongoing**
1. ✅ Check Dashboard daily
2. ✅ AI proactively suggests: "You're 80% to food budget limit"
3. ✅ Make informed decisions

---

## 🔥 **Pro Tips**

### **Tip 1: Upload Regularly**
- Upload bank statements **monthly**
- Keep transaction history updated

### **Tip 2: Use AI Chat**
- Don't hesitate to ask questions
- AI learns from your patterns

### **Tip 3: Set Budgets Early**
- Create budgets in first week
- AI will track automatically

### **Tip 4: Review Subscriptions**
- Check monthly subscriptions
- Cancel unused ones

### **Tip 5: Monitor Anomalies**
- Review unusual transactions
- Verify if legitimate

---

## 📊 **Feature Summary Table**

| **Feature** | **How to Access** | **What It Does** |
|-------------|------------------|------------------|
| Dashboard | Home page | Financial overview |
| Upload PDF | Upload button | Extract transactions |
| Transactions | Header menu | View history |
| AI Chat | Header menu | Ask financial questions |
| Reports | Header menu | Detailed analysis |
| Anomaly Detection | Automatic | Alerts unusual spending |
| Subscriptions | AI page | Identifies recurring payments |
| Budgets | Dashboard | Set spending limits |

---

## 🆘 **Troubleshooting**

### **Problem: Can't login**
**Solution:** 
- Check email/password spelling
- Clear browser cache
- Re-register if needed

### **Problem: PDF upload fails**
**Solution:**
- Check file size (<10MB)
- Ensure it's a PDF file
- Try password-free PDF first

### **Problem: No transactions showing**
**Solution:**
- Upload bank statement first
- Wait 10-15 seconds for processing
- Refresh page

### **Problem: AI not responding**
**Solution:**
- Check if Groq API key is configured
- Verify backend is running
- Check browser console for errors

---

## 🎉 **You're All Set!**

Ab tum **SpendWise AI** ko fully use kar sakte ho! 

**Happy Financial Planning! 💰🚀**
