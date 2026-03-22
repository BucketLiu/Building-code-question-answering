# faiss

This folder stores FAISS vector indexes generated from parsed building code documents.

## Structure

Each subfolder (e.g., `KBxxxxxx/`) corresponds to a distinct knowledge base.  
Inside, you will find:
- `faiss_index/index.faiss` — FAISS index
- `faiss_index/index.pkl` — Metadata (chunk IDs, source information)
