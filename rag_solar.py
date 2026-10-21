import os
import sys
import argparse

# Optimize threading dynamically
threads = str(os.cpu_count() or 4)
for env_var in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "TBB_NUM_THREADS"]:
    os.environ[env_var] = threads

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
chroma_dir = os.path.join(BASE_DIR, "chroma_db")

if not os.path.exists(chroma_dir):
    print(f"Error: Vector database not found at '{chroma_dir}'.")
    print("Please run 'extract_text.py' and then 'store_text.py' first.")
    sys.exit(1)

try:
    import ollama
except ImportError:
    print("Error: 'ollama' python package is required. Run: pip install ollama")
    sys.exit(1)

try:
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma
    except ImportError:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
except ImportError:
    print("Error: LangChain and Chroma dependencies not found. Run: pip install chromadb langchain-community sentence-transformers")
    sys.exit(1)

print("Loading vector embeddings...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(collection_name="textbooks", embedding_function=embedding_model, persist_directory=chroma_dir)

def query_solar(query, model="jeff-ai"):
    # Retrieve top 3 relevant passages
    docs = vector_db.similarity_search(query, k=3)
    if not docs:
        context = "No relevant context found in database."
    else:
        context = "\n\n---\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a specialized AI assistant named Jarvis. Use the following context retrieved from reference documents to answer the question accurately. If the context does not contain sufficient details, state that clearly.

Context:
{context}

Question: {query}
Answer:"""

    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama (model '{model}'): {e}\nEnsure Ollama is running ('ollama serve' or 'systemctl start ollama')."

def main():
    parser = argparse.ArgumentParser(description="Query the Solar RAG document system.")
    parser.add_argument("question", nargs="?", type=str, help="Question to ask the AI (omit for interactive mode).")
    parser.add_argument("--model", type=str, default="jeff-ai", help="Ollama model to query (default: jeff-ai or solar)")
    args = parser.parse_args()

    if args.question:
        print(f"\nQuestion: {args.question}")
        ans = query_solar(args.question, model=args.model)
        print(f"\nResponse:\n{ans}")
    else:
        print("==================================================")
        print("        Solar RAG Interactive Query Shell         ")
        print("==================================================")
        print("Type your question and press Enter. Type 'exit' or 'quit' to end.\n")
        while True:
            try:
                q = input("\nAsk > ").strip()
                if not q:
                    continue
                if q.lower() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break
                print("\nThinking...")
                ans = query_solar(q, model=args.model)
                print(f"\nJarvis: {ans}")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break

if __name__ == "__main__":
    main()
