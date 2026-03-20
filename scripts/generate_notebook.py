import json
import os
import argparse

def generate_notebook(config_path, output_path):
    print(f"📓 Generating Nexus Training Notebook...")
    print(f"Config: {config_path} | Output: {output_path}")

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# NexusLLM: Cloud Training Notebook\n",
                    "This notebook is automatically generated for fine-tuning based on your project configurations."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "!pip install --upgrade \"llamafactory[metrics]\" deepspeed unsloth\n",
                    "!git clone https://github.com/Sharan-G-S/NexusLLM-Unified-Fine-Tuning-Hub-Automated-Deployment-Pipeline.git project\n",
                    "%cd project"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "print('Starting Training...')\n",
                    f"!python3 nexus.py run train --config {config_path} --deepspeed"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(output_path, "w") as f:
        json.dump(notebook, f, indent=2)
    print(f"✅ Notebook generated at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Notebook Generator")
    parser.add_argument("--config", default="configs/qwen2.5/sft_config.yaml", help="Path to config")
    parser.add_argument("--output", default="training_session.ipynb", help="Output path")

    args = parser.parse_args()
    generate_notebook(args.config, args.output)
