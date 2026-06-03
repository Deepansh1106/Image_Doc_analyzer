# Document Fraud Analyzer

An AI-powered document verification system that detects potentially fraudulent or tampered documents using OCR, NLP, metadata analysis, and signature validation.

## Features

* **OCR-Based Text Extraction** – Extracts text from scanned documents and images using Tesseract/EasyOCR.
* **NLP Analysis** – Detects suspicious language patterns, inconsistencies, and anomalies in document content.
* **Metadata Verification** – Analyzes creation/modification history, author details, and editing traces to identify tampering.
* **Signature Validation** – Verifies signatures through image similarity and feature-matching techniques.
* **Image Forensics** – Detects document manipulation using image analysis methods.
* **Fraud Risk Scoring** – Generates an overall fraud score with detailed verification results.

## Tech Stack

* **Backend:** FastAPI, Python
* **OCR:** Tesseract OCR, EasyOCR
* **NLP:** spaCy, Transformers (BERT)
* **Computer Vision:** OpenCV, Pillow
* **Database:** SQLite/PostgreSQL

## Workflow

1. Upload document (PDF/Image)
2. Extract text using OCR
3. Analyze content using NLP
4. Verify document metadata
5. Validate signatures
6. Detect image manipulations
7. Generate fraud risk score and report

## Use Cases

* Identity document verification
* Insurance claim validation
* Financial document auditing
* Recruitment and background verification
* Legal and compliance checks

## Future Improvements

* LLM-powered fraud explanations
* Deepfake document detection
* Multi-language support
* Real-time verification APIs

---

Built to automate document verification and enhance fraud detection through AI-driven analysis.
