# Building-code-question-answering

# Preprocessing & Evaluation Core Code

This folder contains scripts for data preprocessing and evaluating the QA performance.

## Scripts

- `clean_text_preprocessing.py` — Cleans and normalizes parsed Markdown
- `text_split_to_excel_preprocessing.py` — Splits documents into chunks for evaluation
- `evaluation_code.py` — Computes accuracy, BLEU, ROUGE, and BERTScore
- `bert-base-multilingual-cased/` — Tokenizer and config for BERTScore

## Evaluation Metrics

- **Accuracy** — manual expert assessment (required for final judgment)
- **BLEU / ROUGE** — lexical overlap
- **BERTScore** — semantic similarity

