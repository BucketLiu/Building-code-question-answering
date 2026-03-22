# -*- coding: utf-8 -*-
from __future__ import print_function

def get_run_config_params():
    openai_api_base = ""
    openai_api_key = ""
    openai_api_model_name = ""
    openai_api_context_length = "4096"
    workers = 4
    milvus_port = 19530
    qanything_port = 8777
    use_cpu = True
    return "{},{},{},{},{},{},{}".format(openai_api_base, openai_api_key, openai_api_model_name,
                                         openai_api_context_length, workers, milvus_port, qanything_port, use_cpu)

llm_config = {
    "max_token": 512,
    "history_len": 2,
    "token_window": 4096,
    "top_p": 0.8
}

# pdf解析参数
pdf_config = {
    "USE_FAST_PDF_PARSER": True
}

user_defined_configuration = {
    "LOCAL_RERANK_BATCH": 8,
    "LOCAL_RERANK_WORKERS": 4,
    "LOCAL_EMBED_BATCH": 8,
    "LOCAL_EMBED_WORKERS": 4
}

model_config = {
    "SENTENCE_SIZE": 100,
    "CHUNK_SIZE": 800,
    "VECTOR_SEARCH_TOP_K": 40,
    "VECTOR_SEARCH_SCORE_THRESHOLD": 1.1
}
text_splitter_config = {
    "chunk_size": 400,
    "chunk_overlap": 100
}
pdf_splitter_config = {
    "chunk_size": 800,
    "chunk_overlap": 0
}


if __name__ == "__main__":
    import sys
    sys.stdout.write(''.join(get_run_config_params()))