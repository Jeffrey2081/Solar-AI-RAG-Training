import os
os.environ["OMP_NUM_THREADS"] = "12"
os.environ["OPENBLAS_NUM_THREADS"] = "12"
os.environ["MKL_NUM_THREADS"] = "12"
os.environ["NUMEXPR_NUM_THREADS"] = "12"
os.environ["TBB_NUM_THREADS"] = "12"
import ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Load embeddings and vector store
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(collection_name="textbooks", embedding_function=embedding_model, persist_directory="/home/jeff/training/chroma_db")

def query_solar(query):
    # Retrieve most relevant textbook content
    docs = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # Modify the prompt to restrict knowledge
    prompt = f"""
    You are a textbook-trained AI. Only use the following information to answer:
    {context}

    Question: {query}
    """

    # Get response from Solar
    response = ollama.chat(model="solar", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Ask Solar questions
while True:
    query = input("\nAsk a question: ")
    print(query_solar(query))

