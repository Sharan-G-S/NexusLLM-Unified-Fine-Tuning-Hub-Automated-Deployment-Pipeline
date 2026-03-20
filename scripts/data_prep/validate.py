import json
import os
import sys

def validate_jsonl(file_path):
    print(f"Validating {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("Error: Dataset must be a list of objects.")
                return False
            
            for i, entry in enumerate(data):
                if 'instruction' not in entry or 'output' not in entry:
                    print(f"Error: Entry {i} missing required keys ('instruction', 'output').")
                    return False
        
        print(f"Successfully validated {len(data)} entries.")
        return True
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <dataset_path>")
        sys.exit(1)
    
    if validate_jsonl(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1)
