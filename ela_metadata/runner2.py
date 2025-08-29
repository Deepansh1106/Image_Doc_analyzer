#second runner file ( named: runner2.py)
# test_phase2.py
from phase2_ela_metadata import run_phase2_on_pdf

if __name__ == "__main__":
    pdf_path = "/Users/deepansh/SEBI/FakeDoc.pdf"   # replace with your PDF file
    result = run_phase2_on_pdf(pdf_path)

    print("\n--- Phase 2 Scam Check ---")
    print(f"Metadata: {result['metadata']}")
    print(f"Scam Flag: {result['scam_flag']}")
    print("Reasons:")
    for r in result["reasons"]:
        print(f" - {r}")
