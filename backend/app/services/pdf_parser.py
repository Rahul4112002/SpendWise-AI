# PDF parser service
import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() or ""
    return all_text

def is_pdf_encrypted(pdf_path: str) -> bool:
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    return reader.is_encrypted

def decrypt_pdf(pdf_path: str, password: str, output_path: str) -> bool:
    from PyPDF2 import PdfReader, PdfWriter
    reader = PdfReader(pdf_path)
    if reader.is_encrypted:
        try:
            reader.decrypt(password)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            with open(output_path, 'wb') as f:
                writer.write(f)
            return True
        except:
            return False
    return True  # not encrypted
