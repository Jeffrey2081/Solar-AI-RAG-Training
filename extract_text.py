import os
import sys
import json

# Optimize threading dynamically
threads = str(os.cpu_count() or 4)
for env_var in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "TBB_NUM_THREADS"]:
    os.environ[env_var] = threads

try:
    import pypdf
except ImportError:
    print("Error: 'pypdf' package is not installed. Run: pip install pypdf")
    sys.exit(1)

# Dynamic paths relative to script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_folder = os.path.join(BASE_DIR, "pdf")
output_file = os.path.join(BASE_DIR, "extracted_text.json")

os.makedirs(pdf_folder, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text_chunks = []
    try:
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except Exception:
                    print(f"Skipping encrypted PDF: {pdf_path}")
                    return ""
            for idx, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_chunks.append(page_text.strip())
                except Exception as e:
                    print(f"Warning: Failed to extract page {idx + 1} from {pdf_path}: {e}")
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return ""
    return "\n\n".join(text_chunks)

# Scan PDFs
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
if not pdf_files:
    print(f"Notice: No PDF files found in '{pdf_folder}'. Place your PDF files there and rerun.")
    sys.exit(0)

print(f"Found {len(pdf_files)} PDF file(s). Extracting text...")
data = {}
for file in sorted(pdf_files):
    file_path = os.path.join(pdf_folder, file)
    print(f" - Processing: {file}")
    extracted = extract_text_from_pdf(file_path)
    if extracted:
        data[file] = extracted
        print(f"   ✓ Extracted {len(extracted)} characters.")
    else:
        print(f"   ⚠️ No text could be extracted.")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\n✓ Successfully extracted text from {len(data)} document(s) into: {output_file}")
