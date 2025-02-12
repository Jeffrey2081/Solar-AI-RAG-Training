import os
os.environ["OMP_NUM_THREADS"] = "12"
os.environ["OPENBLAS_NUM_THREADS"] = "12"
os.environ["MKL_NUM_THREADS"] = "12"
os.environ["NUMEXPR_NUM_THREADS"] = "12"
os.environ["TBB_NUM_THREADS"] = "12"
import sys
sys.path.append("/home/jeff/.local/lib/python3.13/site-packages")
import pypdf
import os
import json

# Paths
pdf_folder = "/home/jeff/training/pdf/"
output_file = "/home/jeff/training/extracted_text.json"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Extract text from all PDFs and save
data = {}
for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        file_path = os.path.join(pdf_folder, file)
        data[file] = extract_text_from_pdf(file_path)

# Save extracted text as JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"Extracted text saved to {output_file}")

