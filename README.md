# NexusLLM: Unified Fine-Tuning Hub

NexusLLM is a powerful, streamlined environment for fine-tuning Large Language Models (LLMs) and Vision Language Models (VLMs) using **LLaMA-Factory**. It features a **Sectional Push Subsystem** that ensures modular and mistake-free repository management.

## Features
- **Unified Interface**: Supports 100+ models (Llama-3, Mistral, Qwen, etc.).
- **Sectional Push Subsystem**: Automated script to commit/push changes in logical sections (`env`, `data`, `config`, `train`, `eval`).
- **Standardized Workflows**: Pre-configured templates for Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO).

## Getting Started

1. **Initialize the project**:
   ```bash
   python3 nexus.py init
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Manage the repository**:
   Use the `nexus push` command to commit your changes section-by-section:
   ```bash
   python3 nexus.py push env -m "Updated dependencies"
   python3 nexus.py push data -m "Added healthcare dataset"
   python3 nexus.py push config -m "Optimized Llama-3 hyperparameters"
   ```

## Directory Structure
- `configs/`: YAML configurations for fine-tuning.
- `data/`: Datasets and `dataset_info.json`.
- `outputs/`: Training logs and checkpoints.
- `scripts/`: Training and evaluation shell scripts.
- `nexus.py`: The core automation CLI.
