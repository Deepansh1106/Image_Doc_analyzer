#first runner file(named : runner.py)
# For an image upload
from PIL import Image
from phase1_ocr_nlp import run_phase1_on_pdf

#img = Image.open("uploaded_page.jpg")
#result = run_phase1_on_pil(img)
#print(result)

# For a PDF upload
from phase1_ocr_nlp import run_phase1_on_pdf

pdf_result = run_phase1_on_pdf("/Users/deepansh/SEBI/FakeDoc.pdf")
print(pdf_result)

