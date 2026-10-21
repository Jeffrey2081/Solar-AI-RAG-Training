import os
import sys
import json

# Optimize threading dynamically
threads = str(os.cpu_count() or 4)
for env_var in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "TBB_NUM_THREADS"]:
    os.environ[env_var] = threads

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(BASE_DIR, "extracted_text.json")
chroma_dir = os.path.join(BASE_DIR, "chroma_db")

if not os.path.exists(json_file):
    print(f"Error: Extracted text file not found at '{json_file}'.")
    print("Please run 'extract_text.py' first.")
    sys.exit(1)

try:
    with open(json_file, "r", encoding="utf-8") as f:
        textbook_data = json.load(f)
except Exception as e:
    print(f"Error reading {json_file}: {e}")
    sys.exit(1)

if not textbook_data:
    print("Notice: 'extracted_text.json' is empty. Add PDFs to 'pdf/' and rerun 'extract_text.py'.")
    sys.exit(0)

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
except ImportError:
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
    except ImportError:
        print("Error: Required libraries not found. Run: pip install langchain-community chromadb sentence-transformers")
        sys.exit(1)

print("Initializing HuggingFace embedding model (all-MiniLM-L6-v2)...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print(f"Opening ChromaDB at: {chroma_dir}")
vector_db = Chroma(collection_name="textbooks", embedding_function=embedding_model, persist_directory=chroma_dir)

# Simple chunking to prevent embedding context overflow
def chunk_text(text, chunk_size=1000, chunk_overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

print("Indexing documents into ChromaDB...")
total_chunks = 0
for filename, content in textbook_data.items():
    chunks = chunk_text(content)
    if chunks:
        metas = [{"source": filename, "chunk": i} for i in range(len(chunks))]
        vector_db.add_texts(chunks, metadatas=metas)
        total_chunks += len(chunks)
        print(f" - Indexed '{filename}': {len(chunks)} chunks")

if hasattr(vector_db, "persist"):
    vector_db.persist()

print(f"\n✓ Successfully indexed {total_chunks} chunks into ChromaDB at: {chroma_dir}")
