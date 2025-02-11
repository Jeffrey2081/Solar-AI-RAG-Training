import json
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Load extracted text
with open("/home/jeff/training/extracted_text.json", "r", encoding="utf-8") as f:
    textbook_data = json.load(f)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a ChromaDB vector store
vector_db = Chroma(collection_name="textbooks", embedding_function=embedding_model, persist_directory="/home/jeff/training/chroma_db")

# Add textbook data
for filename, content in textbook_data.items():
    vector_db.add_texts([content], metadatas=[{"source": filename}])

vector_db.persist()
print("Textbook data stored in ChromaDB at /home/jeff/training/chroma_db")

