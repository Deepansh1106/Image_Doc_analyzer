# third runner file (named : runner3.py)
from phase3_digital_metadata import run_phase3_on_pdf

pdf_file = "/Users/deepansh/SEBI/testDoc.pdf"  # replace with your PDF
result = run_phase3_on_pdf(pdf_file)

print("Phase 3 Result:")
print("-------------------------")

# Digital signature
sig_status = "Present ✅" if result.get('digital_signature') else "Absent ❌"
print(f"Digital Signature: {sig_status}")

# Broker verification
broker_status = "Verified ✅" if result.get('broker_verified') else "Not Verified ❌"
print(f"Broker Verification: {broker_status}")

# Metadata
print("PDF Metadata:")
for k, v in result.get('metadata', {}).items():
    print(f"  {k}: {v}")

# Optional metadata flag
if 'metadata_flag' in result:
    print(f"Metadata Note: {result['metadata_flag']}")

# Legitimacy
print(f"Legitimacy Score: {result.get('legitimacy')}")
