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
> Due to file size limitations on GitHub, this repository does not include all pre-trained weights and needs to be downloaded separately (please refer to the original paper for source code).