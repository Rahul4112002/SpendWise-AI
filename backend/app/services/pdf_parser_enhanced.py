# Enhanced PDF parser service
import pdfplumber
import re
from datetime import datetime
from typing import Dict, List, Optional
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd

class BankStatementParser:
    """Parser for extracting transaction data from bank statement PDFs"""
    
    def __init__(self):
        self.transaction_patterns = {
            "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            "amount": r"\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b",
            "description": r"[A-Za-z][A-Za-z0-9\s&.-]{3,}",
        }
    
    def is_pdf_encrypted(self, pdf_path: str) -> bool:
        """Check if PDF is password-protected"""
        try:
            reader = PdfReader(pdf_path)
            return reader.is_encrypted
        except Exception as e:
            print(f"Error checking PDF encryption: {e}")
            return False
    
    def decrypt_pdf(self, pdf_path: str, password: str, output_path: str) -> bool:
        """Decrypt password-protected PDF"""
        try:
            reader = PdfReader(pdf_path)
            if reader.is_encrypted:
                if reader.decrypt(password):
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    return True
                else:
                    return False
            return True
        except Exception as e:
            print(f"Error decrypting PDF: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text content from PDF"""
        all_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        
        return all_text
    
    def parse_statement(self, pdf_path: str) -> Dict:
        """Complete statement parsing with metadata extraction"""
        result = {
            "bank_name": None,
            "account_number": None,
            "statement_period": {"start": None, "end": None},
            "transactions": [],
        }
        
        try:
            text = self.extract_text_from_pdf(pdf_path)
            
            # Extract bank name
            bank_patterns = [
                r"(HDFC Bank|ICICI Bank|State Bank of India|SBI|Axis Bank|Kotak Bank|IDFC First Bank)",
            ]
            for pattern in bank_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["bank_name"] = match.group(1)
                    break
            
            # Extract account number
            account_patterns = [
                r"Account\s*(?:No\.?|Number)\s*:?\s*([\dXx*]+)",
            ]
            for pattern in account_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    result["account_number"] = match.group(1)
                    break
            
        except Exception as e:
            print(f"Error parsing statement: {e}")
        
        return result


# Legacy functions for backward compatibility
def extract_text_from_pdf(pdf_path: str) -> str:
    parser = BankStatementParser()
    return parser.extract_text_from_pdf(pdf_path)

def is_pdf_encrypted(pdf_path: str) -> bool:
    parser = BankStatementParser()
    return parser.is_pdf_encrypted(pdf_path)

def decrypt_pdf(pdf_path: str, password: str, output_path: str) -> bool:
    parser = BankStatementParser()
    return parser.decrypt_pdf(pdf_path, password, output_path)
