#!/bin/bash

# Step 1: Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Step 2: Restart terminal by reloading .bashrc
echo "Reloading terminal..."
source ~/.bashrc

# Step 3: Start Ollama server in the background
echo "Starting Ollama server..."
ollama serve &

# Wait for a few seconds to ensure the server starts
sleep 8

# Step 4: Pull Llama 3.1 model
echo "Pulling Llama 3.1 model..."
ollama pull llama3.1

# Step 5: Create a custom model using the provided ModelFile
MODEL_FILE="Modelfile" # Replace with the actual path to your ModelFile
echo "Creating custom model from $MODEL_FILE..."
ollama create llama3.1-tool -f "$MODEL_FILE"

echo "All tasks completed successfully!"
