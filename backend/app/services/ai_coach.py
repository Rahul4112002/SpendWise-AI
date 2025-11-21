# AI recommendations service - Autonomous Financial Coaching Agent
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.core.config import settings

class AutonomousFinancialCoach:
    """
    Autonomous AI Financial Coach that adapts to real user behavior,
    spending patterns, and income variability for gig workers and everyday citizens.
    """
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set in environment variables")
        
        self.llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=0.7,
        )
        
        self.system_prompt = """You are PennyWise AI, an autonomous financial coaching agent designed to help users,
especially gig workers, informal sector employees, and everyday citizens make smarter financial decisions.

Your capabilities:
1. Analyze spending patterns and provide personalized insights
2. Detect anomalies in spending behavior
3. Identify subscriptions and recurring payments
4. Provide proactive budget recommendations based on income variability
5. Suggest savings opportunities
6. Alert users about overspending in specific categories
7. Offer financial coaching adapted to irregular income patterns

Always be:
- Empathetic and supportive
- Practical and actionable
- Clear and concise
- Proactive in identifying issues before they become problems
- Culturally sensitive to diverse financial situations"""
    
    async def analyze_spending_patterns(self, transactions: List[Dict], user_profile: Dict) -> Dict:
        """Analyze user's spending patterns and generate insights"""
        
        total_spent = sum(t.get('amount', 0) for t in transactions if t.get('transaction_type') == 'debit')
        total_income = sum(t.get('amount', 0) for t in transactions if t.get('transaction_type') == 'credit')
        
        category_spending = {}
        for txn in transactions:
            if txn.get('transaction_type') == 'debit':
                cat = txn.get('category', 'uncategorized')
                category_spending[cat] = category_spending.get(cat, 0) + txn.get('amount', 0)
        
        analysis_prompt = f"""
Analyze the following financial data for a {user_profile.get('user_type', 'user')}:

**Monthly Summary:**
- Total Income: ₹{total_income:.2f}
- Total Expenses: ₹{total_spent:.2f}
- Net Savings: ₹{total_income - total_spent:.2f}

**Category-wise Spending:**
{self._format_category_spending(category_spending)}

Provide key insights, concerns, and actionable recommendations.
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=analysis_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "analysis": response.content,
            "metrics": {
                "total_income": total_income,
                "total_expenses": total_spent,
                "net_savings": total_income - total_spent,
                "category_breakdown": category_spending,
            }
        }
    
    async def chat_with_user(self, user_message: str, conversation_history: List[Dict], user_context: Dict) -> str:
        """Interactive chat for financial queries"""
        
        messages = [SystemMessage(content=self.system_prompt)]
        
        for msg in conversation_history[-10:]:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(AIMessage(content=msg['content']))
        
        messages.append(HumanMessage(content=user_message))
        
        response = await self.llm.ainvoke(messages)
        return response.content
    
    async def identify_subscriptions(self, transactions: List[Dict]) -> List[Dict]:
        """Identify recurring subscriptions from transaction data"""
        merchant_groups = {}
        
        for txn in transactions:
            merchant = txn.get('merchant_name', '').lower()
            amount = txn.get('amount', 0)
            
            if merchant and amount > 0:
                key = f"{merchant}_{amount:.2f}"
                if key not in merchant_groups:
                    merchant_groups[key] = []
                merchant_groups[key].append(txn)
        
        subscriptions = []
        for key, txns in merchant_groups.items():
            if len(txns) >= 2:
                subscriptions.append({
                    "merchant": txns[0].get('merchant_name'),
                    "amount": txns[0].get('amount'),
                    "frequency": len(txns),
                    "category": txns[0].get('category'),
                })
        
        return sorted(subscriptions, key=lambda x: x['amount'], reverse=True)
    
    async def detect_anomalies(self, transactions: List[Dict]) -> List[Dict]:
        """Detect unusual spending patterns and anomalies"""
        anomalies = []
        
        if not transactions:
            return anomalies
        
        # Group by category
        category_amounts = {}
        for txn in transactions:
            cat = txn.get('category', 'uncategorized')
            if cat not in category_amounts:
                category_amounts[cat] = []
            category_amounts[cat].append(txn.get('amount', 0))
        
        # Detect anomalies (transactions > 2x average)
        for category, amounts in category_amounts.items():
            if len(amounts) < 3:
                continue
                
            avg = sum(amounts) / len(amounts)
            for txn in transactions:
                if txn.get('category') == category:
                    amount = txn.get('amount', 0)
                    if amount > avg * 2:
                        severity = amount / avg
                        anomalies.append({
                            "category": category,
                            "amount": amount,
                            "average": avg,
                            "severity": severity,
                            "description": f"Spent ₹{amount:.2f} on {category}, which is {severity:.1f}x your average of ₹{avg:.2f}",
                            "merchant": txn.get('merchant_name', 'Unknown'),
                            "date": txn.get('date')
                        })
        
        return sorted(anomalies, key=lambda x: x['severity'], reverse=True)
    
    async def generate_budget_recommendations(self, avg_income: float, category_spending: Dict, user_profile: Dict) -> Dict:
        """Generate AI-powered budget recommendations based on income and spending patterns"""
        
        income_variability = user_profile.get('income_variability', 'stable')
        user_type = user_profile.get('user_type', 'regular_employee')
        
        # Recommended percentages (adjusted for income variability)
        if income_variability == 'highly_variable':
            buffer_pct = 0.30  # 30% emergency buffer for gig workers
        elif income_variability == 'variable':
            buffer_pct = 0.20  # 20% buffer
        else:
            buffer_pct = 0.10  # 10% buffer
        
        # Standard 50/30/20 rule adjusted for income variability
        necessities_pct = 0.50 - buffer_pct
        wants_pct = 0.30
        savings_pct = 0.20 + buffer_pct
        
        budget_prompt = f"""
Create a personalized budget recommendation for a {user_type} with {income_variability} income.

**Income:** ₹{avg_income:.2f}/month

**Current Spending:**
{self._format_category_spending(category_spending)}

**User Profile:**
- Type: {user_type}
- Income Variability: {income_variability}
- Recommended Emergency Buffer: {buffer_pct * 100:.0f}%

Provide specific budget allocations for each category and actionable advice for this user's situation.
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=budget_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        # Calculate recommended allocations
        recommended_budget = {
            "total_income": avg_income,
            "necessities": avg_income * necessities_pct,
            "wants": avg_income * wants_pct,
            "savings_buffer": avg_income * savings_pct,
            "emergency_buffer_pct": buffer_pct * 100,
            "recommendations": response.content,
            "category_limits": self._calculate_category_limits(avg_income, necessities_pct, wants_pct)
        }
        
        return recommended_budget
    
    def _calculate_category_limits(self, income: float, necessities_pct: float, wants_pct: float) -> Dict:
        """Calculate suggested spending limits by category"""
        necessities_amount = income * necessities_pct
        wants_amount = income * wants_pct
        
        return {
            # Necessities
            "groceries": necessities_amount * 0.30,
            "bills": necessities_amount * 0.25,
            "transport": necessities_amount * 0.20,
            "healthcare": necessities_amount * 0.15,
            "education": necessities_amount * 0.10,
            
            # Wants
            "food": wants_amount * 0.40,
            "entertainment": wants_amount * 0.30,
            "shopping": wants_amount * 0.30,
        }
    
    def _format_category_spending(self, category_spending: Dict) -> str:
        """Format category spending for display"""
        lines = []
        for cat, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {cat.title()}: ₹{amount:.2f}")
        return "\n".join(lines) if lines else "No spending data"


# Legacy function
async def get_financial_advice(prompt: str) -> str:
    """Simple financial advice using Groq API"""
    try:
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=0.7,
        )
        
        messages = [
            SystemMessage(content="You are a helpful financial advisor."),
            HumanMessage(content=prompt)
        ]
        
        response = await llm.ainvoke(messages)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
