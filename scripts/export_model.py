import os
import subprocess
import argparse

def export_model(model_path, adapter_path, output_path, export_format="hf"):
    print(f"🚀 Exporting model from {model_path} with adapters from {adapter_path}...")
    print(f"Format: {export_format} | Output: {output_path}")

    # Simplified LLaMA-Factory export command
    cmd = [
        "llamafactory-cli", "export",
        "--model_name_or_path", model_path,
        "--adapter_name_or_path", adapter_path,
        "--template", "qwen",
        "--finetuning_type", "lora",
        "--export_dir", output_path,
        "--export_size", "2",
        "--export_legacy_format", "false"
    ]
    
    if export_format == "gguf":
        cmd.extend(["--export_quantization_bit", "4", "--export_quantization_dataset", "data/finance/sentiment.json"])

    try:
        subprocess.run(cmd, check=True)
        print("✅ Export completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Export failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Model Export & Quantization Utility")
    parser.add_argument("--model", required=True, help="Base model path")
    parser.add_argument("--adapter", required=True, help="Adapter path")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--format", choices=["hf", "gguf"], default="hf", help="Export format")

    args = parser.parse_args()
    export_model(args.model, args.adapter, args.output, args.format)
