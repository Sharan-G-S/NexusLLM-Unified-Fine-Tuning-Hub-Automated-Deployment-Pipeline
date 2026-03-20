import os
import sys
import subprocess
import argparse
import json

class Nexus:
    def __init__(self):
        self.sections = {
            "env": ["requirements.txt", "nexus.py", "README.md", ".gitignore"],
            "data": ["data/", "dataset_info.json", "scripts/data_prep/"],
            "config": ["configs/"],
            "infra": ["deployment/", "configs/deepspeed/"],
            "train": ["outputs/", "scripts/train.sh"],
            "eval": ["outputs/eval/", "scripts/eval.sh"]
        }

    def run_command(self, cmd):
        print(f"Executing: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit(1)

    def init(self):
        print("Initializing Nexus Project...")
        os.makedirs("configs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)
        os.makedirs("scripts", exist_ok=True)
        
        if not os.path.exists("dataset_info.json"):
            with open("dataset_info.json", "w") as f:
                json.dump({}, f, indent=2)
        
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w") as f:
                f.write("outputs/checkpoint-*\n__pycache__/\n*.pyc\n.DS_Store\n")
        
        print("Project initialized successfully.")

    def push(self, section, message):
        if section not in self.sections:
            print(f"Invalid section: {section}. Available: {', '.join(self.sections.keys())}")
            sys.exit(1)

        files = self.sections[section]
        print(f"Staging section: {section}...")
        
        # Check if files exist
        existing_files = []
        for f in files:
            if os.path.exists(f):
                existing_files.append(f)
        
        if not existing_files:
            print(f"No files found for section {section}. Skipping.")
            return

        # Git operations
        self.run_command(["git", "add"] + existing_files)
        commit_msg = f"[SECTION: {section.upper()}] {message}"
        self.run_command(["git", "commit", "-m", commit_msg])
        
        # Check if remote exists before pushing
        try:
            subprocess.run(["git", "remote"], check=True, capture_output=True)
            self.run_command(["git", "push"])
        except subprocess.CalledProcessError:
            print("No remote repository configured. Commit saved locally.")

    def run_train(self, config_path, use_deepspeed=False):
        cmd = ["llamafactory-cli", "train", config_path]
        if use_deepspeed:
            ds_config = "configs/deepspeed/ds_z3_config.json"
            cmd = ["deepspeed", "--num_gpus", "1", "llamafactory-cli", "train", config_path, "--deepspeed", ds_config]
        
        print(f"Starting training with config: {config_path}")
        self.run_command(cmd)

def main():
    parser = argparse.ArgumentParser(description="Nexus: LLaMA-Factory Automation & Push Subsystem")
    subparsers = parser.add_subparsers(dest="command")

    # Init
    subparsers.add_parser("init", help="Initialize project structure")

    # Push
    push_parser = subparsers.add_parser("push", help="Push a specific section to the repository")
    push_parser.add_argument("section", choices=["env", "data", "config", "infra", "train", "eval"], help="Section to push")
    push_parser.add_argument("-m", "--message", required=True, help="Commit message")

    # Run Train
    train_parser = subparsers.add_parser("run", help="Run a training job")
    train_parser.add_argument("action", choices=["train"], help="Action to run")
    train_parser.add_argument("--config", required=True, help="Path to YAML config")
    train_parser.add_argument("--deepspeed", action="store_true", help="Use DeepSpeed ZeRO-3")

    args = parser.parse_args()

    nexus = Nexus()
    if args.command == "init":
        nexus.init()
    elif args.command == "push":
        nexus.push(args.section, args.message)
    elif args.command == "run":
        if args.action == "train":
            nexus.run_train(args.config, args.deepspeed)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
