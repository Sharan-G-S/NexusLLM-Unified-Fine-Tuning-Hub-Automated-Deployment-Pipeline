#!/bin/bash

# Configuration
MODEL_PATH=$1
PORT=${2:-8000}

if [ -z "$MODEL_PATH" ]; then
    echo "Usage: ./serve.sh <model_path_or_adapter_path> [port]"
    exit 1
fi

echo "Starting vLLM Production Server on port $PORT..."
echo "Model: $MODEL_PATH"

# Run vLLM with OpenAI API compatibility
python3 -m vllm.entrypoints.openai.api_server \
    --model "$MODEL_PATH" \
    --served-model-name "nexus-financial-analyst" \
    --port "$PORT" \
    --trust-remote-code \
    --max-model-len 4096 \
    --enforce-eager
