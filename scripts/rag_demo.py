import os
import argparse
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def run_rag_demo(query, document_path):
    print(f"🔍 Initializing RAG Session...")
    print(f"Query: {query}")
    print(f"Data Source: {document_path}")

    # 1. Load an embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 2. Simulate document chunks
    documents = [
        "NVIDIA's revenue grew by 265% in Q4 2024.",
        "Apple's services business hit an all-time high of $23.1 billion.",
        "Microsoft surpassed a $3 trillion market cap.",
        "The Federal Reserve maintained interest rates at 5.25%-5.50%."
    ]

    # 3. Create FAISS index
    embeddings = model.encode(documents)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))

    # 4. Search
    query_vector = model.encode([query])
    D, I = index.search(query_vector.astype('float32'), k=1)
    context = documents[I[0][0]]

    print(f"✅ Retrieved Context: {context}")
    print(f"🤖 Prompting Nexus Model with context...")
    # Simulation: In production, this would call the vLLM endpoint
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer (based on context only):"
    print(f"Generated Prompt:\n{prompt}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus RAG Integration Demo")
    parser.add_argument("--query", required=True, help="User query")
    parser.add_argument("--docs", default="data/finance/sentiment.json", help="Path to documents")

    args = parser.parse_args()
    run_rag_demo(args.query, args.docs)
