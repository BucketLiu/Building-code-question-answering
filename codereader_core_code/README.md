# codereader_core_code

This folder contains the core implementation of CodeReader, which parses building code documents (PDFs, images) into clean Markdown.

## Key Components

- Layout analysis (YOLOv8)
- Text detection & recognition (PSENet + CRNN)
- Table recognition (SLANet)
- Formula recognition (UniMERNet)
- Information fusion and Markdown generation

Refer to the script comments for details.

> ⚠️ This folder includes the core code and pre-trained model configurations.  
>
> Pre-trained weights are not included in this repository and need to be downloaded separately (see the original paper for sources).