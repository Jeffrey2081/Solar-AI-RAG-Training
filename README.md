# RAG Training Setup with Solar and ChromaDB

This repository contains a setup for training and running a **Retrieval-Augmented Generation (RAG)** system using **OLAMA Solar**, **ChromaDB**, and **Hugging Face sentence embeddings**.

## Features
- Extracts text from PDFs and saves it as JSON.
- Uses **ChromaDB** to store and retrieve vectorized text data.
- Uses **OLAMA Solar** as the LLM for answering questions.
- Optimized for fast retrieval with `sentence-transformers/all-MiniLM-L6-v2`.

## 🛠 Installation

### Install Required Packages

<details>
<summary>📦 Fedora</summary>

```sh
sudo dnf install python3.13 python3.13-pip
```
</details>

<details>
<summary>📦 Debian/Ubuntu</summary>

```sh
sudo apt install python3.13 python3.13-pip
```
</details>

<details>
<summary>📦 Arch Linux</summary>

```sh
sudo pacman -S python python-pip
```
</details>

### Install Python Dependencies
Run the following command to install required packages:

```sh
pip install pypdf langchain-community chromadb sentence-transformers ollama
```
Due to occasional issues you might need to use ``` --break-system-packages ```
### Install and Run OLAMA

<details>
<summary>📦 Fedora / Debian / Ubuntu / Arch</summary>

```sh
curl -fsSL https://ollama.com/install.sh | sh
```
</details>

After installation, start the OLAMA service:

```sh
ollama pull solar
```

```sh
ollama run solar
```

For more details, refer to the official OLAMA repository: [Ollama GitHub](https://github.com/ollama/ollama)

## 📂 File Structure

```
/home/jeff/training/
├── extract_text.py   # Extracts text from PDFs
├── store_text.py     # Indexes extracted text into ChromaDB
├── rag_solar.py      # Queries OLAMA Solar using RAG
├── extracted_text.json  # Extracted text data (generated)
├── chroma_db/        # ChromaDB storage
└── pdf/              # Folder containing input PDFs
```

## 🚀 Usage

### 1️⃣ Extract Text from PDFs
Ensure your PDFs are inside:

```
/home/jeff/training/pdf/
```

Then run:

```sh
python /home/jeff/training/extract_text.py
```

This will create a JSON file:

```
/home/jeff/training/extracted_text.json
```

### 2️⃣ Index Text Data into ChromaDB
Run the following command:

```sh
python /home/jeff/training/store_text.py
```

This will store the extracted text as vector embeddings inside:

```
/home/jeff/training/chroma_db/
```

### 3️⃣ Run the Query System
Start querying the RAG system with:

```sh
python /home/jeff/training/rag_solar.py
```

You can now ask questions based on the indexed textbook data.

## ⚙️ Environment Optimization

For better performance, threading optimizations are applied in `rag_solar.py`:

```python
import os
os.environ["OMP_NUM_THREADS"] = "12"
os.environ["OPENBLAS_NUM_THREADS"] = "12"
os.environ["MKL_NUM_THREADS"] = "12"
os.environ["NUMEXPR_NUM_THREADS"] = "12"
os.environ["TBB_NUM_THREADS"] = "12"
```

Adjust these values based on your CPU.

## 📝 Configuration

If you move the training setup to a different location, update **all file paths** inside:

- `extract_text.py`
- `store_text.py`
- `rag_solar.py`

Replace:

```python
pdf_folder = "/home/jeff/training/pdf/"
output_file = "/home/jeff/training/extracted_text.json"
persist_directory="/home/jeff/training/chroma_db"
```

with the new directory paths and where ever there is 'jeff' replace with your home directory 

## 🔧 Future Improvements
- ✅ Implement a GUI interface for easier interaction.
- ✅ Add multi-document chunking for better context handling.
- ✅ Expand to support multiple embedding models.

## 📢 Follow My Journey
For updates and insights on my Arch Linux setup and RAG experiments.

[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/jeffrey__2081/)

---
