# Building Code Question Answering

This repository contains the large language model fine-tuning dataset and core code implementation of the BuildingQA framework introduced in the paper:

> **"Intelligent Building Code Question Answering Framework Augmented by Multimodal Document Parsing and Fine-Grained Retrieval-Augmented Large Language Model"**
>
> The application of building code knowledge is critical to ensuring building safety, compliance, and sustainability. However, owing to the enormous volume of provisions and intricate layouts inherent in building code documents, current research on building code question answering (QA) confronts prominent challenges, such as suboptimal retrieval performance and responses with inadequate alignment to the original text. Therefore, we propose an intelligent building code QA framework augmented by multimodal document parsing and fine-grained retrieval-augmented large language model (LLM). This framework primarily comprises the following core components: (i) CodeReader, a novel building code multimodal document parsing method via hybrid deep learning, is developed. This method integrates multiple tasks, including layout analysis, text interpretation, formula recognition and table recognition, to achieve unified representation of heterogeneous information in code documents. (ii) A fine-grained retrieval-augmented generation method is established by combining dual-encoders and cross-encoders. The framework enhances the semantic discrimination of similar provisions in building codes through joint encoding of retrieval results and questions, as well as reranking of initial retrieval outputs. (iii) We construct a specialized LLM fine-tuning dataset tailored to building code QA tasks. Leveraging this dataset, we fine-tune a base LLM via low-rank adaptation, yielding BuildingQA-7B, a domain-specific model with enhanced semantic understanding and generation capabilities for code content. Evaluated on the hydraulic building code QA task, the proposed framework achieves an accuracy of 91.67%, a BLEU score of 0.216, and maintains a reasoning latency of 2.05 s. It outperforms comparison methods in terms of accuracy, semantic similarity, and response speed. Finally, a graphical user interface is developed to integrate the aforementioned modules, facilitating intuitive interactive questioning and reliable source traceability. This study provides a new solution for intelligent acquisition and efficient application of building code knowledge, contributing to the automation of building code understanding and application.

The system provides an intelligent approach for querying building codes, combining:
- **CodeReader**: multimodal document parser for building codes  

- **FG-RAG**: fine-grained retrieval-augmented generation  

- **BuildingQA-7B**: a domain-specific LLM fine-tuned for code question answering

  <img src="figures\Research framework.png" alt="Research framework" style="zoom:20%;" />

## 📂 Repository Structure

Building-code-question-answering/
├── building_code_data/ # Parsed documents & fine-tuning dataset
├── codereader_core_code/ # Core parsing code (CodeReader)
├── faiss/ # Vector index storage
├── generation_core_code/ # Retrieval, LLM inference & GUI
└── preprocessing_and_evaluation_core_code/ # Preprocessing & evaluation scripts

## 📖 Citation

If you use this data or core code, please cite our paper:

@article{liu2025buildingqa,
  title={Intelligent Building Code Question Answering Framework Augmented by Multimodal Document Parsing and Fine-Grained Retrieval-Augmented Large Language Model},
  author={Liu, Leping and Ren, Qiubing and Li, Mingchao and Yu, Yantao and Lv, Yuangeng and Kong, Rui and Zhang, Xiaojian},
  journal={Journal of Computing in Civil Engineering}, 
  volume={xxx},
  number={xx},
  pages={xxxxx},
  year={2026}
}