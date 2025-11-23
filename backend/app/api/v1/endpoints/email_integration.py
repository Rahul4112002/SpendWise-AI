# Email Integration Endpoints for Bank Statement Automation
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.models.bank_statement import BankStatement
from app.services.email_parser import EmailStatementParser, generate_password_variants

router = APIRouter()


class EmailCredentials(BaseModel):
    email: EmailStr
    app_password: str
    imap_server: Optional[str] = None  # Auto-detect
    days: int = 60


class PDFPasswordInfo(BaseModel):
    """User info for unlocking password-protected bank PDFs"""
    date_of_birth: Optional[str] = None  # DDMMYYYY format
    mobile_number: Optional[str] = None
    account_number: Optional[str] = None
    pan_card: Optional[str] = None
    custom_password: Optional[str] = None


class FetchStatementsRequest(BaseModel):
    email_credentials: EmailCredentials
    pdf_password_info: Optional[PDFPasswordInfo] = None
    bank_name: Optional[str] = None


class EmailSyncResponse(BaseModel):
    total_emails_fetched: int
    statements_found: int
    statements_processed: int
    transactions_extracted: int
    failed_pdfs: List[str]
    message: str


@router.post("/fetch-statements", response_model=EmailSyncResponse)
async def fetch_bank_statements_from_email(
    request: FetchStatementsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    **Automated Bank Statement Fetching from Email**
    
    Automatically fetches and processes bank statements from your email.
    
    **📧 Email Setup (Gmail):**
    1. Go to Google Account → Security
    2. Enable 2-Step Verification
    3. Generate App Password for "Mail"
    4. Use that 16-character password (not your Gmail password)
    
    **🔐 Password-Protected PDFs:**
    Most banks protect PDFs with:
    - Date of Birth (DDMMYYYY) - Most common
    - Last 4 digits of mobile
    - Last 4 digits of account number
    - PAN card number
    
    Provide your details and we'll try common patterns automatically!
    
    **🏦 Supported Banks:**
    ICICI, HDFC, Axis, SBI, Kotak, Yes Bank, IndusInd, BOB, PNB, Canara, Union, IDBI
    """
    try:
        creds = request.email_credentials
        pdf_info = request.pdf_password_info
        
        # Initialize email parser
        parser = EmailStatementParser(
            email_address=creds.email,
            email_password=creds.app_password,
            imap_server=creds.imap_server
        )
        
        # Fetch bank statement emails
        emails_data = parser.fetch_bank_statement_emails(
            days=creds.days,
            bank_name=request.bank_name
        )
        
        statements_processed = 0
        total_transactions = 0
        failed_pdfs = []
        
        # Process each email with PDF attachments
        for email_data in emails_data:
            bank = email_data['bank']
            
            for attachment in email_data['attachments']:
                pdf_data = attachment['data']
                filename = attachment['filename']
                
                try:
                    # Try to unlock PDF
                    unlocked_pdf = parser.try_unlock_pdf(
                        pdf_data=pdf_data,
                        bank=bank,
                        user_dob=pdf_info.date_of_birth if pdf_info else None,
                        user_mobile=pdf_info.mobile_number if pdf_info else None,
                        user_account=pdf_info.account_number if pdf_info else None,
                        user_pan=pdf_info.pan_card if pdf_info else None,
                        custom_password=pdf_info.custom_password if pdf_info else None
                    )
                    
                    if unlocked_pdf is None:
                        failed_pdfs.append(f"{filename} (Password not matched)")
                        continue
                    
                    # Parse transactions from PDF
                    parsed_data = parser.parse_statement_from_pdf(unlocked_pdf)
                    
                    # Save bank statement record
                    statement = BankStatement(
                        user_id=current_user.id,
                        filename=filename,
                        file_path=f"email_import/{email_data['email_id']}",
                        file_size=len(pdf_data),
                        bank_name=bank,
                        is_processed=True,
                        processing_status="completed",
                        total_transactions=parsed_data['total_transactions']
                    )
                    db.add(statement)
                    db.flush()
                    
                    # Save transactions
                    for trans in parsed_data['transactions']:
                        # Determine transaction type
                        debit_amt = float(trans['debit']) if trans['debit'] != "0.00" else 0
                        credit_amt = float(trans['credit']) if trans['credit'] != "0.00" else 0
                        
                        amount = debit_amt if debit_amt > 0 else credit_amt
                        trans_type = "debit" if debit_amt > 0 else "credit"
                        
                        transaction = Transaction(
                            user_id=current_user.id,
                            amount=amount,
                            transaction_type=trans_type,
                            description=trans['description'],
                            merchant_name=trans['description'][:50],  # First 50 chars
                            transaction_date=datetime.strptime(trans['date'], "%d/%d/%Y") if "/" in trans['date'] else datetime.now(),
                            bank_name=bank,
                            from_sms=False,
                            category="uncategorized"
                        )
                        db.add(transaction)
                        total_transactions += 1
                    
                    statements_processed += 1
                    
                except Exception as e:
                    failed_pdfs.append(f"{filename} ({str(e)})")
                    continue
        
        db.commit()
        
        return EmailSyncResponse(
            total_emails_fetched=len(emails_data),
            statements_found=sum(len(e['attachments']) for e in emails_data),
            statements_processed=statements_processed,
            transactions_extracted=total_transactions,
            failed_pdfs=failed_pdfs,
            message=f"✅ Processed {statements_processed} statements, extracted {total_transactions} transactions!"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-sms-csv")
async def upload_sms_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload SMS backup CSV file
    
    **CSV Format:**
    ```
    timestamp,sender,message
    2024-01-15 10:30:00,HDFCBK,Your A/c XX1234 debited Rs.500...
    ```
    
    **How to Export SMS:**
    - Android: Use "SMS Backup & Restore" app
    - Export as CSV format
    - Upload here
    """
    try:
        # Save uploaded file temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Parse CSV
        transactions = SMSFileParser.parse_csv(tmp_path)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        transactions_added = 0
        
        # Save to database
        for trans_data in transactions:
            # Check duplicates
            existing = db.query(Transaction).filter(
                Transaction.user_id == current_user.id,
                Transaction.amount == trans_data['amount'],
                Transaction.merchant_name == trans_data['merchant_name']
            ).first()
            
            if not existing:
                transaction = Transaction(
                    user_id=current_user.id,
                    amount=trans_data['amount'],
                    transaction_type=trans_data['transaction_type'],
                    merchant_name=trans_data.get('merchant_name', 'Unknown'),
                    description=trans_data.get('description', ''),
                    transaction_date=datetime.now(),
                    from_sms=True,
                    sms_sender=trans_data.get('sms_sender'),
                    raw_sms_text=trans_data.get('raw_sms_text'),
                    bank_name=trans_data.get('bank_name'),
                    account_last4=trans_data.get('account_last4'),
                    category=trans_data.get('category', 'uncategorized')
                )
                db.add(transaction)
                transactions_added += 1
        
        db.commit()
        
        return {
            "total_sms": len(transactions),
            "transactions_added": transactions_added,
            "message": f"✅ Successfully imported {transactions_added} transactions from SMS backup!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse CSV: {str(e)}")


@router.post("/upload-sms-xml")
async def upload_sms_xml(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload SMS backup XML file (Android format)
    
    **XML Format:** Standard Android SMS Backup format
    
    **How to Export:**
    - Use "SMS Backup & Restore" app on Android
    - Export as XML
    - Upload here
    """
    try:
        import tempfile
        import os
        
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Parse XML
        transactions = SMSFileParser.parse_xml(tmp_path)
        
        # Clean up
        os.unlink(tmp_path)
        
        transactions_added = 0
        
        # Save to database
        for trans_data in transactions:
            existing = db.query(Transaction).filter(
                Transaction.user_id == current_user.id,
                Transaction.amount == trans_data['amount'],
                Transaction.merchant_name == trans_data['merchant_name']
            ).first()
            
            if not existing:
                transaction = Transaction(
                    user_id=current_user.id,
                    amount=trans_data['amount'],
                    transaction_type=trans_data['transaction_type'],
                    merchant_name=trans_data.get('merchant_name', 'Unknown'),
                    description=trans_data.get('description', ''),
                    transaction_date=datetime.now(),
                    from_sms=True,
                    sms_sender=trans_data.get('sms_sender'),
                    raw_sms_text=trans_data.get('raw_sms_text'),
                    bank_name=trans_data.get('bank_name'),
                    account_last4=trans_data.get('account_last4'),
                    category=trans_data.get('category', 'uncategorized')
                )
                db.add(transaction)
                transactions_added += 1
        
        db.commit()
        
        return {
            "total_sms": len(transactions),
            "transactions_added": transactions_added,
            "message": f"✅ Successfully imported {transactions_added} transactions from SMS backup!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse XML: {str(e)}")
