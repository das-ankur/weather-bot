echo "Downloading and installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Step 4: Configure Ollama to run as a service
echo "Configuring Ollama to run as a service..."
sudo bash -c 'cat > /etc/systemd/system/ollama.service <<EOF
[Unit]
Description=Ollama Service
After=network.target

[Service]
ExecStart=/usr/local/bin/ollama serve --host 0.0.0.0 --port 11434
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF'

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl start ollama
sudo systemctl enable ollama

# Step 5: Pull a model (example: llama2-uncensored)
echo "Pulling the Llama2-Uncensored model..."
ollama pull llama2-uncensored