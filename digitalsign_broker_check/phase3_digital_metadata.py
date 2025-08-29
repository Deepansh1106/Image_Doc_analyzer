# phase3_digital_metadata.py
import fitz  # type: ignore # PyMuPDF
import sqlite3
import pytesseract # type: ignore
from pdf2image import convert_from_path # type: ignore
from PIL import Image # type: ignore
import re

# --- Helper: Digital signature check with signer extraction ---
def check_digital_signature(pdf_path):
    """
    Returns dict with presence of signature and signer CN (common name).
    """
    result = {"present": False, "signer": None}

    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            annot = page.firstAnnot
            while annot:
                if annot.type[0] == 20:  # Signature annotation
                    result["present"] = True
                    sig_info = annot.info  # Metadata about the signature
                    signer = sig_info.get("title") or sig_info.get("subject") or sig_info.get("name")
                    result["signer"] = signer
                annot = annot.next
        doc.close()
    except Exception as e:
        print("Error checking digital signature:", e)

    return result

# --- Helper: OCR for broker info ---
def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    full_text = ""
    for page in pages:
        img = page.convert('RGB')
        text = pytesseract.image_to_string(img)
        full_text += text + "\n"
    return full_text

# --- Helper: Verify broker against DB (by reg_no + name) ---
def verify_broker(name, reg_no, db_path='broker_db.sqlite'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM brokers WHERE registration_no=? AND name=?", (reg_no, name))
    result = c.fetchone()
    conn.close()
    return result is not None

# --- Helper: Verify signer name directly in broker DB ---
def verify_signer_in_db(signer, db_path='broker_db.sqlite'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM brokers WHERE name=?", (signer,))
    result = c.fetchone()
    conn.close()
    return result is not None

# --- Main Phase3 function ---
def run_phase3_on_pdf(pdf_path, db_path='broker_db.sqlite'):
    result = {}

    # Step 1: Digital signature extraction
    signature_info = check_digital_signature(pdf_path)
    result['digital_signature'] = signature_info
    legitimacy_score = 0.5  # base score

    if signature_info["present"]:
        legitimacy_score += 0.2
        signer = signature_info["signer"]

        if signer and verify_signer_in_db(signer, db_path):
            legitimacy_score += 0.3
            signature_info["trusted"] = True
        else:
            legitimacy_score -= 0.2
            signature_info["trusted"] = False
    else:
        signature_info["trusted"] = False

    # Step 2: Broker verification via OCR
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

    # Step 3: Final legitimacy classification
    result['legitimacy'] = round(legitimacy_score, 2)
    return result
