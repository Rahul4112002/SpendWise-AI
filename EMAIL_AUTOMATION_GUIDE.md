# 📧 Email-Based Bank Statement Automation - Complete Guide

## 🎯 **Feature Overview**

**Automatic bank statement fetching and processing from your email!**

Instead of manual PDF uploads, this feature:
1. ✅ Connects to your Gmail/Yahoo
2. ✅ Scans last 60 days for bank statement emails
3. ✅ Downloads PDF attachments automatically
4. ✅ Unlocks password-protected PDFs using common patterns
5. ✅ Extracts all transactions
6. ✅ Saves to your account

---

## 🚀 **How to Use**

### **Step 1: Gmail App Password Setup**

**Important:** You CANNOT use your regular Gmail password! You need an "App Password"

#### **Setup Process:**
1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already)
3. Search for **"App Passwords"**
4. Click **"Select app"** → Choose **"Mail"**
5. Click **"Select device"** → Choose **"Other"** → Type "PennyWise"
6. Click **"Generate"**
7. Copy the **16-character password** (looks like: `xxxx xxxx xxxx xxxx`)
8. Save it somewhere safe!

### **Step 2: Access Email Sync**

1. Login to SpendWise AI
2. Click **"📧 Email Sync"** in the header menu
3. You'll see a 3-step process

### **Step 3: Enter Email Credentials**

**Form Fields:**
- **Email Address**: `your.email@gmail.com`
- **App Password**: Paste the 16-character password from Step 1
- **Fetch Last**: Choose 60 days (recommended)

Click **"Next: PDF Password Info →"**

### **Step 4: PDF Password Information**

Most Indian banks password-protect their PDF statements. Provide your info so we can unlock them automatically:

**Common Patterns:**

| **Bank** | **Common Password** | **Example** |
|----------|---------------------|-------------|
| ICICI, HDFC, Axis, SBI | Date of Birth (DDMMYYYY) | 15041990 |
| Kotak | DOB (DDMMYY) | 150490 |
| Yes Bank | Account Last 4 | 1234 |
| IndusInd | PAN Card | ABCDE1234F |

**Fill the form:**
- **Date of Birth**: `15041990` (DDMMYYYY format)
- **Mobile Number**: Your 10-digit number or last 4 digits
- **Account Number**: Last 4 digits (optional)
- **PAN Card**: Your PAN (optional)
- **Custom Password**: If you know exact password

**Don't worry!** System will try multiple combinations automatically.

Click **"🚀 Fetch & Process Statements"**

### **Step 5: Results**

You'll see:
```
✅ Processed 3 statements, extracted 127 transactions!

📊 Stats:
- Emails Scanned: 45
- Statements Found: 5
- Successfully Processed: 3
- Transactions Extracted: 127
```

If some PDFs failed:
```
⚠️ Failed PDFs (2):
- statement_nov.pdf (Password not matched)
- oct_statement.pdf (Corrupted file)
```

**What to do:**
- Upload failed PDFs manually
- Or update password info and try again

---

## 🔐 **Password Patterns Explained**

### **How It Works:**

When we find a password-protected PDF, we try:

1. **Your custom password** (if provided)
2. **Common bank patterns**:
   - DOB: `15041990`
   - DOB Short: `150490`
   - DOB Alpha: `15apr1990`
   - Mobile Last 4: `1234`
   - Account Last 4: `5678`
   - PAN: `ABCDE1234F`

### **Supported Banks:**

✅ **Full Support:**
- ICICI Bank
- HDFC Bank
- Axis Bank
- State Bank of India (SBI)
- Kotak Mahindra Bank
- Yes Bank
- IndusInd Bank
- Bank of Baroda (BOB)
- Punjab National Bank (PNB)
- Canara Bank
- Union Bank
- IDBI Bank

---

## 📝 **Example Workflow**

### **Scenario:** Rahul wants to import 3 months of ICICI statements

**Step 1: Email Setup**
```
Email: rahul@gmail.com
App Password: abcd efgh ijkl mnop
Days: 90
```

**Step 2: PDF Password**
```
Date of Birth: 15041990
(ICICI uses DOB as password)
```

**Step 3: Fetch**
- System finds 3 ICICI emails
- Downloads 3 PDFs
- Tries password: `15041990` ✅ Success!
- Extracts 89 transactions

**Step 4: View Transactions**
- Click "View Transactions →"
- All 89 transactions appear in history
- Already categorized by AI!

---

## ⚠️ **Troubleshooting**

### **Problem 1: "Email connection failed"**

**Solutions:**
- ✅ Check if App Password is correct (not regular password)
- ✅ Verify 2-Step Verification is enabled
- ✅ Generate a new App Password
- ✅ For Yahoo: Use Yahoo-specific App Password

### **Problem 2: "Password not matched"**

**Solutions:**
- ✅ Verify your DOB format (DDMMYYYY, not DD/MM/YYYY)
- ✅ Try entering custom password
- ✅ Check with your bank for PDF password pattern
- ✅ Upload PDF manually instead

### **Problem 3: "No statements found"**

**Solutions:**
- ✅ Increase "Fetch Last Days" to 90 or 180
- ✅ Check if bank sends statements to this email
- ✅ Verify email inbox has statement emails
- ✅ Search your email for "statement" keyword

### **Problem 4: "Transactions not extracted"**

**Solutions:**
- ✅ PDF might have scanned images (not parsable)
- ✅ Try newer statement (OCR coming soon)
- ✅ Upload manually and we'll extract

---

## 🔒 **Security & Privacy**

### **Is it safe?**

**YES! Here's why:**

1. **App Passwords are revocable**
   - Can be deleted anytime from Google Account
   - Limited to "Mail" access only
   - No access to other Google services

2. **No storage of passwords**
   - Your App Password is never saved
   - Used only during fetch operation
   - Immediately discarded after use

3. **PDF passwords**
   - Used only to unlock PDFs
   - Not stored anywhere
   - Only kept in memory during processing

4. **Local processing**
   - PDFs processed on our servers
   - Not shared with third parties
   - Deleted after transaction extraction

### **Best Practices:**

✅ **DO:**
- Use App Passwords (not regular passwords)
- Revoke App Password after use if concerned
- Keep DOB/PAN info private

❌ **DON'T:**
- Share App Password with others
- Use same password everywhere
- Keep App Password in plain text

---

## 🎁 **Benefits**

### **vs Manual Upload:**

| **Feature** | **Manual** | **Email Automation** |
|------------|------------|---------------------|
| Find statements | You search emails | ✅ Auto-scans |
| Download PDFs | Manual | ✅ Automatic |
| Unlock passwords | Try manually | ✅ Smart unlock |
| Extract transactions | Upload one-by-one | ✅ Batch process |
| Time taken | 10-15 mins | ✅ 30 seconds |

### **Use Cases:**

1. **Monthly Ritual**
   - Run once a month
   - Fetch last 30 days
   - All transactions auto-imported

2. **First-time Setup**
   - Fetch last 180 days
   - Import 6 months history
   - Complete financial picture

3. **Multiple Banks**
   - All statements in one email
   - Process all together
   - Unified transaction view

---

## 📊 **What Happens After Import?**

1. **Transactions appear** in Transaction History
2. **AI automatically categorizes** (Food, Transport, Shopping, etc.)
3. **Anomaly detection** runs (unusual spending alerts)
4. **Subscription detection** identifies recurring payments
5. **Budget recommendations** get updated
6. **Dashboard** shows updated stats

**You just login, fetch, and your finances are up-to-date! 🎉**

---

## 🆘 **Support**

### **Common Questions:**

**Q: How often should I sync?**
A: Once a month is perfect. Or whenever you get a new statement email.

**Q: Can I use Yahoo/Outlook?**
A: Yes! System auto-detects IMAP server. Just provide email and app password.

**Q: What if my bank isn't listed?**
A: Try "Custom Password" or upload manually. We'll add your bank pattern!

**Q: Will this work for credit cards?**
A: Yes! Most credit card statements work the same way.

**Q: Can I delete imported transactions?**
A: Yes, go to Transactions page and delete individually.

---

## 🎯 **Next Steps**

1. ✅ Setup Gmail App Password
2. ✅ Go to Email Sync page
3. ✅ Enter credentials
4. ✅ Provide DOB
5. ✅ Fetch statements
6. ✅ View transactions
7. ✅ Let AI analyze your spending!

**Happy Automated Financial Tracking! 📧💰**
