import json
from phase1_ocr_nlp import run_phase1_on_pdf
from phase2_ela_metadata import run_phase2_on_pdf
from phase3_digital_metadata import run_phase3_on_pdf


def calculate_risk_score(ocr_score, scam_flag, legitimacy_score):
    """
    Combine the three phase outputs into a final risk score (0–100).
    If scam_flag (modified) is True → give it higher weight dynamically.
    """

    ocr_component = ocr_score                       # already 0–100
    legitimacy_component = (1 - legitimacy_score) * 100  # higher legitimacy = lower risk

    # Adjust weights depending on scam_flag
    if scam_flag:
        weights = {"ocr": 0.25, "mod": 0.50, "leg": 0.25}   # more weight to modification
    else:
        weights = {"ocr": 0.40, "mod": 0.20, "leg": 0.40}   # balanced if not modified

    # Risk score calculation
    risk_score = (
        weights["ocr"] * ocr_component +
        weights["mod"] * (100 if scam_flag else 0) +  # modification risk = binary high signal
        weights["leg"] * legitimacy_component
    )

    return round(risk_score, 2)


def run_all(pdf_path):
    # --- Phase 1: OCR + NLP scam detection ---
    phase1_result = run_phase1_on_pdf(pdf_path)
    scam_analysis = phase1_result.get("scam_analysis", {})
    ocr_text_scam_score = scam_analysis.get("risk_score", 0)

    # --- Phase 2: ELA/metadata (file modification detection) ---
    phase2_result = run_phase2_on_pdf(pdf_path)
    scam_flag = phase2_result.get("scam_flag", False)

    # --- Phase 3: Digital metadata ---
    phase3_result = run_phase3_on_pdf(pdf_path)
    legitimacy_score = phase3_result.get("legitimacy", 0.0)  # expected 0–1

    # --- Final risk score ---
    final_risk_score = calculate_risk_score(ocr_text_scam_score, scam_flag, legitimacy_score)

    # --- Collect signals ---
    signals = []
    signals.extend(scam_analysis.get("signals", []))
    signals.append(f"document_modified: {scam_flag}")
    signals.append(f"legitimacy_score: {legitimacy_score:.2f}")

    return {
        "risk_score": final_risk_score,
        "signals": signals
    }


if __name__ == "__main__":
    pdf_file = "give_path"   # update with actual file path
    result = run_all(pdf_file)
    print(json.dumps(result, indent=2))
