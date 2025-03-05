import argparse
import ollama
from langchain_chroma import Chroma
import os
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["OMP_NUM_THREADS"] = "12"
os.environ["OPENBLAS_NUM_THREADS"] = "12"
os.environ["MKL_NUM_THREADS"] = "12"
os.environ["NUMEXPR_NUM_THREADS"] = "12"
os.environ["TBB_NUM_THREADS"] = "12"

# Load embeddings and vector store
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(collection_name="textbooks", embedding_function=embedding_model, persist_directory="/home/jeff/Solar-AI-RAG-Training/chroma_db")

def query_solar(query):
    # Retrieve most relevant textbook content
    docs = vector_db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # Modify the prompt to restrict knowledge
    prompt = f"""
    You are a pdf-trained AI. Your main work is to tell the or guess the disease based on the symptoms and your name is Jarvis . Only use the following information to answer:
    {context}

    Question: {query}
    """

    # Get response from Solar
    response = ollama.chat(model="jeff-ai", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def main():
    parser = argparse.ArgumentParser(description="Ask a question to the RAG system.")
    parser.add_argument("question", type=str, help="The question you want to ask.")
    args = parser.parse_args()

    # Ask the question and print the response
    response = query_solar(args.question)
    print(args.question)
    print(response)

if __name__ == "__main__":
    main()

