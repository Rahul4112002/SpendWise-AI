# Email-based Bank Statement Parser
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import os
import re
from typing import List, Dict, Optional
import PyPDF2
import pdfplumber
from io import BytesIO

class EmailStatementParser:
    """
    Parse bank statements from email automatically
    Supports password-protected PDFs with common bank patterns
    """
    
    # Common bank password patterns (Indian banks)
    BANK_PASSWORD_PATTERNS = {
        "ICICI": ["DOB_DDMMYYYY", "DOB_ddmmmyyyy"],  # e.g., 15041990, 15apr1990
        "HDFC": ["DOB_DDMMYYYY", "PANCARD_LAST4"],
        "AXIS": ["DOB_DDMMYYYY", "MOBILE_LAST4"],
        "SBI": ["DOB_DDMMYYYY", "ACCOUNT_LAST4"],
        "KOTAK": ["DOB_DDMMYY", "MOBILE_LAST4"],
        "YES": ["DOB_DDMMYYYY"],
        "INDUSIND": ["PANCARD", "DOB_DDMMYYYY"],
        "BOB": ["DOB_DDMMYYYY"],  # Bank of Baroda
        "PNB": ["DOB_DDMMYYYY"],  # Punjab National Bank
        "CANARA": ["DOB_DDMMYYYY"],
        "UNION": ["DOB_DDMMYYYY"],
        "IDBI": ["DOB_DDMMYYYY"],
        "DEFAULT": ["DOB_DDMMYYYY", "MOBILE_LAST4", "ACCOUNT_LAST4"]
    }
    
    def __init__(self, email_address: str, email_password: str, imap_server: str = None):
        """
        Initialize email parser
        
        Args:
            email_address: User's email (Gmail/Yahoo)
            email_password: Email app password (not regular password)
            imap_server: IMAP server address (auto-detected for Gmail/Yahoo)
        """
        self.email_address = email_address
        self.email_password = email_password
        
        # Auto-detect IMAP server
        if imap_server is None:
            if "gmail" in email_address.lower():
                self.imap_server = "imap.gmail.com"
            elif "yahoo" in email_address.lower():
                self.imap_server = "imap.mail.yahoo.com"
            elif "outlook" in email_address.lower() or "hotmail" in email_address.lower():
                self.imap_server = "outlook.office365.com"
            else:
                self.imap_server = imap_server
        else:
            self.imap_server = imap_server
    
    def connect_to_email(self) -> imaplib.IMAP4_SSL:
        """Connect to email server"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_address, self.email_password)
            return mail
        except Exception as e:
            raise Exception(f"Email connection failed: {str(e)}")
    
    def fetch_bank_statement_emails(self, days: int = 60, bank_name: str = None) -> List[Dict]:
        """
        Fetch emails containing bank statements
        
        Args:
            days: Look back period (default: 60 days)
            bank_name: Filter by specific bank (optional)
        
        Returns:
            List of emails with PDF attachments
        """
        mail = self.connect_to_email()
        mail.select("inbox")
        
        # Calculate date range
        since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
        
        # Search criteria - Bank statement keywords
        search_keywords = [
            "statement",
            "account statement",
            "bank statement",
            "e-statement",
            "monthly statement"
        ]
        
        if bank_name:
            search_keywords.append(bank_name.lower())
        
        emails_data = []
        
        for keyword in search_keywords:
            # Search for emails
            status, messages = mail.search(None, f'(SINCE {since_date} SUBJECT "{keyword}")')
            
            if status == "OK":
                email_ids = messages[0].split()
                
                for email_id in email_ids[-10:]:  # Last 10 emails
                    try:
                        status, msg_data = mail.fetch(email_id, "(RFC822)")
                        
                        if status == "OK":
                            email_body = msg_data[0][1]
                            email_message = email.message_from_bytes(email_body)
                            
                            # Extract email details
                            subject = self._decode_subject(email_message["Subject"])
                            from_email = email_message.get("From")
                            date = email_message.get("Date")
                            
                            # Extract bank name from sender
                            detected_bank = self._detect_bank_from_email(from_email, subject)
                            
                            # Check for PDF attachments
                            attachments = self._extract_pdf_attachments(email_message)
                            
                            if attachments:
                                emails_data.append({
                                    "email_id": email_id.decode(),
                                    "subject": subject,
                                    "from": from_email,
                                    "date": date,
                                    "bank": detected_bank,
                                    "attachments": attachments
                                })
                    
                    except Exception as e:
                        print(f"Error processing email {email_id}: {str(e)}")
                        continue
        
        mail.close()
        mail.logout()
        
        return emails_data
    
    def _decode_subject(self, subject: str) -> str:
        """Decode email subject"""
        if subject is None:
            return ""
        
        decoded_parts = decode_header(subject)
        decoded_subject = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_subject += part.decode(encoding or "utf-8")
                except:
                    decoded_subject += part.decode("utf-8", errors="ignore")
            else:
                decoded_subject += part
        
        return decoded_subject
    
    def _detect_bank_from_email(self, from_email: str, subject: str) -> str:
        """Detect bank name from sender email or subject"""
        from_email = from_email.lower() if from_email else ""
        subject = subject.lower() if subject else ""
        
        bank_keywords = {
            "ICICI": ["icici", "icicibank"],
            "HDFC": ["hdfc", "hdfcbank"],
            "AXIS": ["axis", "axisbank"],
            "SBI": ["sbi", "onlinesbi", "statebankofindia"],
            "KOTAK": ["kotak", "kotakbank"],
            "YES": ["yesbank", "yes bank"],
            "INDUSIND": ["indusind"],
            "BOB": ["bankofbaroda", "bob"],
            "PNB": ["pnb", "pnbindia"],
            "CANARA": ["canara", "canarabank"],
            "UNION": ["unionbank"],
            "IDBI": ["idbi", "idbibank"]
        }
        
        for bank, keywords in bank_keywords.items():
            for keyword in keywords:
                if keyword in from_email or keyword in subject:
                    return bank
        
        return "UNKNOWN"
    
    def _extract_pdf_attachments(self, email_message) -> List[Dict]:
        """Extract PDF attachments from email"""
        attachments = []
        
        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            
            if part.get("Content-Disposition") is None:
                continue
            
            filename = part.get_filename()
            
            if filename and filename.lower().endswith(".pdf"):
                attachments.append({
                    "filename": filename,
                    "data": part.get_payload(decode=True)
                })
        
        return attachments
    
    def try_unlock_pdf(
        self, 
        pdf_data: bytes, 
        bank: str, 
        user_dob: str = None,
        user_mobile: str = None,
        user_account: str = None,
        user_pan: str = None,
        custom_password: str = None
    ) -> Optional[bytes]:
        """
        Try to unlock password-protected PDF using common patterns
        
        Args:
            pdf_data: PDF file bytes
            bank: Bank name
            user_dob: Date of birth (DDMMYYYY format)
            user_mobile: Mobile number (last 4 digits)
            user_account: Account number (last 4 digits)
            user_pan: PAN card number
            custom_password: User-provided password
        
        Returns:
            Unlocked PDF bytes or None
        """
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_data))
        
        # Check if PDF is encrypted
        if not pdf_reader.is_encrypted:
            return pdf_data
        
        # Try custom password first
        if custom_password:
            if pdf_reader.decrypt(custom_password):
                return self._save_unlocked_pdf(pdf_reader)
        
        # Get password patterns for bank
        patterns = self.BANK_PASSWORD_PATTERNS.get(bank, self.BANK_PASSWORD_PATTERNS["DEFAULT"])
        
        # Generate possible passwords
        possible_passwords = []
        
        for pattern in patterns:
            if pattern == "DOB_DDMMYYYY" and user_dob:
                possible_passwords.append(user_dob)
            
            elif pattern == "DOB_DDMMYY" and user_dob:
                possible_passwords.append(user_dob[-6:])  # Last 6 digits
            
            elif pattern == "DOB_ddmmmyyyy" and user_dob:
                # Convert to format like "15apr1990"
                try:
                    date_obj = datetime.strptime(user_dob, "%d%m%Y")
                    formatted = date_obj.strftime("%d%b%Y").lower()
                    possible_passwords.append(formatted)
                except:
                    pass
            
            elif pattern == "MOBILE_LAST4" and user_mobile:
                possible_passwords.append(user_mobile[-4:])
            
            elif pattern == "ACCOUNT_LAST4" and user_account:
                possible_passwords.append(user_account[-4:])
            
            elif pattern == "PANCARD" and user_pan:
                possible_passwords.append(user_pan.upper())
            
            elif pattern == "PANCARD_LAST4" and user_pan:
                possible_passwords.append(user_pan[-4:].upper())
        
        # Try all possible passwords
        for password in possible_passwords:
            try:
                if pdf_reader.decrypt(password):
                    print(f"✅ PDF unlocked with password pattern: {password[:2]}***")
                    return self._save_unlocked_pdf(pdf_reader)
            except:
                continue
        
        # If still locked, return None
        return None
    
    def _save_unlocked_pdf(self, pdf_reader: PyPDF2.PdfReader) -> bytes:
        """Save unlocked PDF to bytes"""
        output_pdf = PyPDF2.PdfWriter()
        
        for page in pdf_reader.pages:
            output_pdf.add_page(page)
        
        output_stream = BytesIO()
        output_pdf.write(output_stream)
        output_stream.seek(0)
        
        return output_stream.read()
    
    def parse_statement_from_pdf(self, pdf_data: bytes) -> Dict:
        """
        Parse transactions from unlocked PDF
        
        Returns:
            Dictionary with extracted transactions
        """
        transactions = []
        
        try:
            with pdfplumber.open(BytesIO(pdf_data)) as pdf:
                full_text = ""
                
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"
                
                # Extract transactions using regex patterns
                # Common patterns for Indian bank statements
                patterns = [
                    # Date, Description, Debit, Credit, Balance
                    r'(\d{2}/\d{2}/\d{4})\s+([A-Za-z0-9\s\-/]+?)\s+(\d+\.\d{2}|\-)\s+(\d+\.\d{2}|\-)\s+(\d+\.\d{2})',
                    # Date, Description, Amount, Type
                    r'(\d{2}-\d{2}-\d{4})\s+([A-Za-z0-9\s\-/]+?)\s+(Dr|Cr)\s+(\d+\.\d{2})',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, full_text, re.MULTILINE)
                    
                    for match in matches:
                        if len(match) >= 4:
                            transactions.append({
                                "date": match[0],
                                "description": match[1].strip(),
                                "debit": match[2] if match[2] != "-" else "0.00",
                                "credit": match[3] if len(match) > 3 and match[3] != "-" else "0.00"
                            })
        
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
        
        return {
            "total_transactions": len(transactions),
            "transactions": transactions
        }


# Helper function to generate password patterns
def generate_password_variants(dob: str = None, mobile: str = None, pan: str = None) -> List[str]:
    """
    Generate all possible password variants based on user data
    
    Args:
        dob: Date of birth (DDMMYYYY)
        mobile: Mobile number
        pan: PAN card number
    
    Returns:
        List of possible passwords
    """
    passwords = []
    
    if dob:
        passwords.extend([
            dob,  # 15041990
            dob[-6:],  # 041990 (DDMMYY)
            dob[-4:],  # 1990 (YYYY)
        ])
        
        # Date formats
        try:
            date_obj = datetime.strptime(dob, "%d%m%Y")
            passwords.extend([
                date_obj.strftime("%d%b%Y").lower(),  # 15apr1990
                date_obj.strftime("%d%b%Y").upper(),  # 15APR1990
                date_obj.strftime("%d%m%y"),  # 150490
            ])
        except:
            pass
    
    if mobile:
        passwords.extend([
            mobile[-4:],  # Last 4 digits
            mobile,  # Full number
        ])
    
    if pan:
        passwords.extend([
            pan.upper(),  # ABCDE1234F
            pan[-4:],  # 1234
        ])
    
    return passwords
