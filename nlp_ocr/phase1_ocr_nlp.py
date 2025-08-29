import cv2
import numpy as np
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Hugging Face Transformers
from transformers import pipeline

# --- Load Phishing Detector (BERT fine-tuned) ---
phishing_model = pipeline(
    "text-classification",
    model="ealvaradob/bert-finetuned-phishing",
    tokenizer="ealvaradob/bert-finetuned-phishing"
)

# --- PDF to Images ---
def pdf_to_images(pdf_path, dpi=300):
    return convert_from_path(pdf_path, dpi=dpi)

# --- Preprocessing (OpenCV) ---
def preprocess_image(pil_img):
    img = np.array(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Threshold + denoise
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)

    return denoised

# --- OCR ---
def run_ocr(image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

# --- NLP Scam Detector (Improved) ---
def scam_detector(text, phishing_threshold=0.85):
    if not text.strip():
        return {
            "risk_score": 0,
            "signals": ["no_text_detected"]
        }

    # --- Split into chunks of ~500 chars (model limit ~512 tokens) ---
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    phishing_probs = []
    legit_probs = []

    for chunk in chunks:
        result = phishing_model(chunk, truncation=True)[0]
        label = result["label"].lower()
        score = float(result["score"])

        if label == "phishing":
            phishing_probs.append(score)
            legit_probs.append(1 - score)
        else:
            phishing_probs.append(1 - score)
            legit_probs.append(score)

    # --- Aggregate results ---
    avg_phishing_prob = np.mean(phishing_probs)
    avg_legit_prob = np.mean(legit_probs)

    # --- Apply threshold to avoid false positives ---
    if avg_phishing_prob > phishing_threshold:
        risk_score = int(avg_phishing_prob * 100)
        scam_detected = True
    else:
        risk_score = int(avg_phishing_prob * 70)  # dampen false alarms
        scam_detected = False

    # --- Prepare signals ---
    signals = [
        f"ocr_text_scam_score: {round(avg_phishing_prob, 2)}",
        f"scam_detected: {scam_detected}"
    ]

    return {
        "risk_score": risk_score,
        "signals": signals
    }

# --- Run Phase 1 on PDF ---
def run_phase1_on_pdf(pdf_path):
    pages = pdf_to_images(pdf_path, dpi=300)
    full_text = ""

    for page in pages:
        processed = preprocess_image(page)
        text = run_ocr(processed)
        full_text += text + "\n"

    scam_result = scam_detector(full_text)

    return {
        "scam_analysis": scam_result
    }
