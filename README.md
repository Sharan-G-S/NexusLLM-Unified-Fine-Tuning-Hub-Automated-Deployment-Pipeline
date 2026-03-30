# NexusLLM: Financial Intelligence Edition (Test):

NexusLLM is a high-performance environment for fine-tuning **Financial Intelligence** models using **LLaMA-Factory**. It is optimized for specializing models like **Qwen-2.5** for financial sentiment analysis, market trend reasoning, and automated investment insights.

## Features
- **Project Focus**: Financial Intelligence (Sentiment, Market Analysis).
- **Core Model**: Qwen-2.5-7B (Specialized for reasoning).
- **Sectional Push Subsystem**: Modular repository management via `nexus.py`.
- **Unified Pipeline**: Pre-configured for Supervised Fine-Tuning (SFT).

## Getting Started

1. **Initialize the project**:
   ```bash
   python3 nexus.py init
   ```

2. **Manage the repository**:
   Use the `nexus push` command to commit your changes section-by-section:
   ```bash
   python3 nexus.py push data -m "Added finance sentiment dataset"
   python3 nexus.py push config -m "Added Qwen-2.5 finance sft config"
   ```

## Financial Data
- `data/finance/sentiment.json`: Targeted financial sentiment training data.
- `dataset_info.json`: LLaMA-Factory link for the finance dataset.

## Configuration
- `configs/qwen2.5/sft_config.yaml`: Optimized hyperparameters for Qwen-2.5 on financial tasks.
  
-----
