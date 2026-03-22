# Building-code-question-answering

# Generation Core Code

This module implements the **FG-RAG** retrieval-augmented generation pipeline and the **BuildingQA-7B** model.

## Components

- `kernel/` — Core retrieval, embedding, reranking, and LLM inference logic
- `llm_finetuning.py` — Script for LoRA fine-tuning
- `run_for_BuildingQA_7B.sh` — Script to start the QA service (GUI)
- `QA_BuildingQA_7B.ipynb` — Interactive notebook for testing

## Models

- Embedding: `bce-embedding-base_v1`
- Reranker: `bce-reranker-base_v1`
- Base LLM: `Qwen-7B-Chat`
- Fine-tuned adapter: `BuildingQA-7B` (LoRA)

Refer to the script comments for details.

> ⚠️ This folder includes the core code.  
>
> Due to file size limitations on GitHub uploads, model files are not included in this repository and need to be downloaded separately (access provided in the original paper).