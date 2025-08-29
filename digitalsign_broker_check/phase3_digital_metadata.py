# phase3_digital_metadata.py
import fitz  # PyMuPDF
import sqlite3
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re

# --- Helper: Extract PDF Metadata ---
def get_pdf_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    meta = doc.metadata
    doc.close()
    return meta

# --- Helper: Digital signature check ---
def has_digital_signature(pdf_path):
    """
    Returns True if PDF has any digital signature.
    """
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            annot = page.firstAnnot
            while annot:
                # 20 is signature annotation type in PyMuPDF
                if annot.type[0] == 20:
                    doc.close()
                    return True
                annot = annot.next
        doc.close()
        return False
    except Exception as e:
        print("Error checking digital signature:", e)
        return False

# --- Helper: OCR for broker info ---
def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""
    for page in pages:
        img = page.convert('RGB')
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
    return full_text

# --- Helper: Verify broker against DB ---
def verify_broker(name, reg_no, db_path='broker_db.sqlite'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM brokers WHERE registration_no=? AND name=?", (reg_no, name))
    result = c.fetchone()
    conn.close()
    return result is not None

# --- Main Phase3 function ---
def run_phase3_on_pdf(pdf_path, db_path='broker_db.sqlite'):
    result = {}

    # Step 1: Digital signature
    signature_exists = has_digital_signature(pdf_path)
    result['digital_signature'] = signature_exists
    legitimacy_score = 0.5  # default medium

    if signature_exists:
        legitimacy_score += 0.4  # signed docs are more trustworthy

    # Step 2: Metadata analysis
    meta = get_pdf_metadata(pdf_path)
    result['metadata'] = meta

    if meta.get('modDate') != meta.get('creationDate'):
        legitimacy_score -= 0.2
        result['metadata_flag'] = 'Document modified after creation'

    # Step 3: Broker verification via OCR
    text = extract_text_from_pdf(pdf_path)
    reg_match = re.search(r'IN[A-Z0-9]{9}', text)
    name_match = re.search(r'(?i)Name[:\s]*([A-Za-z &]+)', text)

    broker_verified = False
    if reg_match and name_match:
        reg_no = reg_match.group()
        name = name_match.group(1).strip()
        broker_verified = verify_broker(name, reg_no, db_path)
        if broker_verified:
            legitimacy_score += 0.3
        else:
            legitimacy_score -= 0.2
    result['broker_verified'] = broker_verified

    # Step 4: Final legitimacy classification
    
    result['legitimacy'] = legitimacy_score
    return result
