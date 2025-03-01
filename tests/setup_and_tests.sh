#!/bin/bash

# Script to automate setup, build, run, and test Quantum Intelligence apps

echo "Starting Quantum Intelligence setup and testing..."

# --- Directory Setup ---
BASE_DIR=~/Desktop/Quantum-1/Quantum-Vedang
cd $BASE_DIR || { echo "Directory $BASE_DIR not found!"; exit 1; }

# --- 1. Install Dependencies ---
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt || { echo "Dependency installation failed!"; exit 1; }
# Optional: Manual TensorFlow install if requirements.txt fails
# pip install tensorflow==2.15.0

# System dependencies for TensorFlow (Pop!_OS/Ubuntu)
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-dev python3-pip libatlas-base-dev

# --- 2. Build Docker Images ---
echo "Building Docker image for app.py..."
docker build -t quantum-app:latest -f Dockerfile . || { echo "Build failed for quantum-app!"; exit 1; }

echo "Building Docker image for apiapp.py..."
docker build -t quantum-api:latest -f Dockerfile.api . || { echo "Build failed for quantum-api!"; exit 1; }

# --- 3. Stop and Remove Existing Containers ---
echo "Stopping and removing any existing containers..."
docker stop quantum-app-container quantum-api-container || true
docker rm quantum-app-container quantum-api-container || true

# --- 4. Run Docker Containers ---
echo "Running quantum-app container (port 5000)..."
docker run -d -p 5000:5000 --name quantum-app-container quantum-app:latest || { echo "Failed to run quantum-app!"; exit 1; }

echo "Running quantum-api container (port 7777)..."
docker run -d -p 7777:7777 --name quantum-api-container quantum-api:latest || { echo "Failed to run quantum-api!"; exit 1; }

# Wait a few seconds for containers to start
sleep 5

# --- 5. Verify Containers ---
echo "Checking container status..."
docker ps -a

# --- 6. Generate JWT Token ---
echo "Generating JWT token from /api/auth..."
TOKEN=$(curl -k -s -X POST -H "Content-Type: application/json" -d '{"api_key": "test-key"}' https://localhost:7777/api/auth | grep -o '"token":"[^"]*' | cut -d'"' -f4)
if [ -z "$TOKEN" ]; then
    echo "Failed to generate token! Check logs:"
    docker logs quantum-api-container
    exit 1
fi
export TOKEN
echo "JWT Token: $TOKEN"

# --- 7. Test app.py Endpoints (Port 5000) ---
echo "Testing app.py endpoints..."
echo "1. /generate_entropy"
curl -k "https://localhost:5000/generate_entropy?seed=42"
echo -e "\n"

echo "2. /encrypt"
ENCRYPTED=$(curl -k -s -X POST -H "Content-Type: application/json" -d '{"data": "hello"}' https://localhost:5000/encrypt | grep -o '"encrypted_data":"[^"]*' | cut -d'"' -f4)
echo "{\"encrypted_data\": \"$ENCRYPTED\"}"
echo -e "\n"

echo "3. /decrypt"
curl -k -X POST -H "Content-Type: application/json" -d "{\"encrypted_data\": \"$ENCRYPTED\"}" https://localhost:5000/decrypt
echo -e "\n"

echo "4. /predict"
curl -k -X POST -H "Content-Type: application/json" -d '{"value": 42}' https://localhost:5000/predict
echo -e "\n"

# --- 8. Test apiapp.py Endpoints (Port 7777) ---
echo "Testing apiapp.py endpoints..."
echo "1. /api/auth (already tested, token saved)"
echo -e "\n"

echo "2. /api/process-signal"
curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"signal_data": [1, 2, 3, 4, 5]}' https://localhost:7777/api/process-signal
echo -e "\n"

echo "3. /api/detect-anomalies"
curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"data": [1, 2, 3, 4, 5], "threshold": 0.8}' https://localhost:7777/api/detect-anomalies
echo -e "\n"

echo "4. /api/encrypt"
curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"data": "secret"}' https://localhost:7777/api/encrypt
echo -e "\n"

echo "5. /api/quantum-intelligence"
curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"data_stream": [1, 2, 3, 4, 5]}' https://localhost:7777/api/quantum-intelligence
echo -e "\n"

echo "6. /api/metrics"
curl -k -H "X-API-Key: $TOKEN" https://localhost:7777/api/metrics
echo -e "\n"

# --- 9. Check Logs (Optional) ---
echo "Container logs can be checked with:"
echo "docker logs quantum-app-container"
echo "docker logs quantum-api-container"

echo "Setup and testing complete!"