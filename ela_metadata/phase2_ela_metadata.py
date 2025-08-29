# phase2_pdf_metadata.py
from PyPDF2 import PdfReader

def run_phase2_on_pdf(pdf_path: str):
    # Extract metadata
    reader = PdfReader(pdf_path)
    metadata = reader.metadata or {}

    scam_flag = False
    reasons = []

    # 1. Check modification vs creation date
    if '/ModDate' in metadata and '/CreationDate' in metadata:
        if metadata['/ModDate'] != metadata['/CreationDate']:
            scam_flag = True
            reasons.append("Modification date differs from creation date (file may have been edited).")

    # 2. Check if Author or Producer is missing
    if '/Author' not in metadata or not metadata['/Author']:
        scam_flag = True
        reasons.append("Author information is missing (suspicious if expected).")

    if '/Producer' not in metadata or not metadata['/Producer']:
        scam_flag = True
        reasons.append("Producer information is missing (could indicate stripped metadata).")

    # 3. Check for suspicious software mentions (e.g., Photoshop, Illustrator)
    suspicious_tools = ["Adobe Photoshop","Adobe Illustrator","Adobe Acrobat","GIMP","Inkscape","CorelDRAW","Paint.NET","Affinity Photo","Canva","Sejda","Smallpdf","ILovePDF","Foxit","Nitro PDF","PDFescape","PDF-XChange","Scribus","Preview","OpenOffice"]
    for key, value in metadata.items():
        if any(tool.lower() in str(value).lower() for tool in suspicious_tools):
            scam_flag = True
            reasons.append(f"Suspicious software detected in metadata: {value}")

    # 4. Inconsistent timestamps check
    if '/CreationDate' in metadata and '/ModDate' in metadata:
        if metadata['/CreationDate'] > metadata['/ModDate']:
            scam_flag = True
            reasons.append("Creation date is later than modification date (timestamp inconsistency).")

    return {
        "metadata": metadata,
        "scam_flag": scam_flag,
        "reasons": reasons
    }
