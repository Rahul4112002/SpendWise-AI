# SMS forwarding handler service
import re
from datetime import datetime
from typing import Dict, Optional, List
import json

class SMSParser:
    \"\"\"Parser for extracting transaction information from bank SMS messages\"\"\"
    
    # Common patterns for Indian banks
    BANK_PATTERNS = {
        \"amount\": [
            r\"(?:Rs\\.?|INR|₹)\\s*([\\d,]+\\.?\\d*)\",
            r\"(?:amount|amt)\\s*(?:of)?\\s*(?:Rs\\.?|INR|₹)?\\s*([\\d,]+\\.?\\d*)\",
            r\"([\\d,]+\\.?\\d*)\\s*(?:Rs\\.?|INR|₹)\",
        ],
        \"transaction_type\": [
            (r\"debited|debit|spent|paid|purchase|withdrawal\", \"debit\"),
            (r\"credited|credit|received|deposited|refund\", \"credit\"),
        ],
        \"account\": [
            r\"(?:A\\/c|account|a\\/c)\\s*(?:no\\.?|number)?\\s*(?:xx|ending|\\*{2,})?([\\dXx*]{4,})\",
            r\"card\\s*(?:ending|no\\.?)\\s*([\\d*]{4})\",
        ],
        \"merchant\": [
            r\"(?:at|to|from)\\s+([A-Z][A-Z0-9\\s&.-]+?)(?:\\s+on|\\.\\s|\\,|\$)\",
            r\"(?:merchant|vendor):\\s*([A-Z][A-Za-z0-9\\s&.-]+)\",
        ],
        \"date\": [
            r\"(\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4})\",
            r\"(\\d{1,2}\\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\s+\\d{2,4})\",
        ],
        \"bank_name\": [
            r\"(?:^|\\b)(HDFC|ICICI|SBI|Axis|Kotak|IDFC|PNB|BOB|Canara|Union|HSBC|Citi|Standard Chartered)(?:\\s+Bank)?(?:\\b|$)\",
        ],
    }
    
    # Category keywords for auto-categorization
    CATEGORY_KEYWORDS = {
        \"food\": [\"restaurant\", \"cafe\", \"zomato\", \"swiggy\", \"food\", \"dominos\", \"pizza\", \"mcdonald\", \"kfc\", \"subway\"],
        \"transport\": [\"uber\", \"ola\", \"rapido\", \"metro\", \"railway\", \"irctc\", \"fuel\", \"petrol\", \"diesel\", \"parking\"],
        \"shopping\": [\"amazon\", \"flipkart\", \"myntra\", \"ajio\", \"mall\", \"store\", \"shop\"],
        \"bills\": [\"electricity\", \"water\", \"gas\", \"broadband\", \"internet\", \"mobile\", \"recharge\", \"postpaid\"],
        \"entertainment\": [\"netflix\", \"prime\", \"hotstar\", \"spotify\", \"movie\", \"cinema\", \"theatre\"],
        \"healthcare\": [\"hospital\", \"pharmacy\", \"medical\", \"doctor\", \"clinic\", \"medicine\"],
        \"education\": [\"school\", \"college\", \"university\", \"course\", \"udemy\", \"coursera\"],
        \"groceries\": [\"supermarket\", \"grocery\", \"bigbasket\", \"grofers\", \"dmart\", \"reliance fresh\"],
    }
    
    def parse_sms(self, sms_text: str, sender: str) -> Optional[Dict]:
        \"\"\"Parse SMS text and extract transaction details\"\"\"
        try:
            # Extract amount
            amount = self._extract_amount(sms_text)
            if not amount:
                return None
            
            # Extract transaction type
            transaction_type = self._extract_transaction_type(sms_text)
            
            # Extract account info
            account = self._extract_account(sms_text)
            
            # Extract merchant/description
            merchant = self._extract_merchant(sms_text)
            
            # Extract date
            transaction_date = self._extract_date(sms_text)
            
            # Extract bank name
            bank_name = self._extract_bank_name(sms_text, sender)
            
            # Auto-categorize
            category = self._categorize_transaction(merchant, sms_text)
            
            return {
                \"amount\": amount,
                \"transaction_type\": transaction_type,
                \"merchant_name\": merchant,
                \"category\": category,
                \"transaction_date\": transaction_date,
                \"bank_name\": bank_name,
                \"account_last4\": account,
                \"from_sms\": True,
                \"sms_sender\": sender,
                \"raw_sms_text\": sms_text,
            }
        except Exception as e:
            print(f\"Error parsing SMS: {e}\")
            return None
    
    def _extract_amount(self, text: str) -> Optional[float]:
        \"\"\"Extract amount from SMS text\"\"\"
        for pattern in self.BANK_PATTERNS[\"amount\"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(\",\", \"\")
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        return None
    
    def _extract_transaction_type(self, text: str) -> str:
        \"\"\"Determine if transaction is debit or credit\"\"\"
        for pattern, txn_type in self.BANK_PATTERNS[\"transaction_type\"]:
            if re.search(pattern, text, re.IGNORECASE):
                return txn_type
        return \"debit\"  # Default to debit
    
    def _extract_account(self, text: str) -> Optional[str]:
        \"\"\"Extract account number (last 4 digits)\"\"\"
        for pattern in self.BANK_PATTERNS[\"account\"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                account = match.group(1)
                # Get last 4 digits
                digits = re.findall(r\"\\d\", account)
                if len(digits) >= 4:
                    return \"\".join(digits[-4:])
        return None
    
    def _extract_merchant(self, text: str) -> Optional[str]:
        \"\"\"Extract merchant name from SMS\"\"\"
        for pattern in self.BANK_PATTERNS[\"merchant\"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                merchant = match.group(1).strip()
                # Clean up merchant name
                merchant = re.sub(r\"\\s+\", \" \", merchant)
                return merchant[:100]  # Limit length
        return \"Unknown Merchant\"
    
    def _extract_date(self, text: str) -> datetime:
        \"\"\"Extract transaction date from SMS\"\"\"
        for pattern in self.BANK_PATTERNS[\"date\"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                try:
                    # Try different date formats
                    for fmt in [\"%d/%m/%Y\", \"%d-%m-%Y\", \"%d/%m/%y\", \"%d %b %Y\", \"%d %B %Y\"]:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
                except Exception:
                    pass
        return datetime.utcnow()  # Default to current time
    
    def _extract_bank_name(self, text: str, sender: str) -> Optional[str]:
        \"\"\"Extract bank name from SMS\"\"\"
        # First try from sender ID
        for pattern in self.BANK_PATTERNS[\"bank_name\"]:
            match = re.search(pattern, sender, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Then try from SMS text
        for pattern in self.BANK_PATTERNS[\"bank_name\"]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _categorize_transaction(self, merchant: Optional[str], text: str) -> str:
        \"\"\"Auto-categorize transaction based on merchant and keywords\"\"\"
        search_text = f\"{merchant or ''} {text}\".lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in search_text:
                    return category
        
        return \"uncategorized\"
    
    def detect_recurring_pattern(self, transactions: List[Dict]) -> List[Dict]:
        \"\"\"Detect recurring transactions (subscriptions)\"\"\"
        # Group transactions by merchant and amount
        grouped = {}
        for txn in transactions:
            key = f\"{txn.get('merchant_name', 'unknown')}_{txn.get('amount', 0)}\"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(txn)
        
        recurring = []
        for key, txns in grouped.items():
            if len(txns) >= 2:
                # Check if transactions occur at regular intervals
                dates = [t.get('transaction_date') for t in txns if t.get('transaction_date')]
                if len(dates) >= 2:
                    # Simple check: if we have multiple transactions, mark as recurring
                    recurring.append({
                        \"merchant\": txns[0].get('merchant_name'),
                        \"amount\": txns[0].get('amount'),
                        \"frequency\": len(txns),
                        \"pattern\": \"monthly\",  # Simplified
                    })
        
        return recurring


class SMSForwardingHandler:
    \"\"\"Handler for processing forwarded SMS messages\"\"\"
    
    def __init__(self):
        self.parser = SMSParser()
    
    async def process_sms(self, sms_text: str, sender: str, user_id: int) -> Optional[Dict]:
        \"\"\"Process a forwarded SMS and extract transaction data\"\"\"
        parsed_data = self.parser.parse_sms(sms_text, sender)
        
        if parsed_data:
            parsed_data[\"user_id\"] = user_id
            return parsed_data
        
        return None
    
    async def bulk_process_sms(self, sms_list: List[Dict], user_id: int) -> List[Dict]:
        \"\"\"Process multiple SMS messages at once\"\"\"
        transactions = []
        
        for sms in sms_list:
            result = await self.process_sms(
                sms.get(\"text\", \"\"),
                sms.get(\"sender\", \"\"),
                user_id
            )
            if result:
                transactions.append(result)
        
        return transactions
