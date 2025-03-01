#!/bin/bash

# Standalone script to test Quantum Intelligence APIs (app.py and apiapp.py)
# Assumes Docker containers (quantum-app-container on port 5000, quantum-api-container on port 7777) are running

BASE_DIR=~/Desktop/Quantum-1/Quantum-Vedang
cd $BASE_DIR || { echo "Directory $BASE_DIR not found!"; exit 1; }

echo "Starting Quantum Intelligence API testing..."

# --- Verify Containers Are Running ---
echo "Checking container status..."
docker ps -a | grep -E "quantum-app-container|quantum-api-container" || { echo "Containers not running! Start them with docker run commands."; exit 1; }

# --- Generate JWT Token (if not already set) ---
echo "Generating JWT token from /api/auth..."
TOKEN=$(curl -k -s -X POST -H "Content-Type: application/json" -d '{"api_key": "test-key"}' https://localhost:7777/api/auth | grep -o '"token":"[^"]*' | cut -d'"' -f4)
if [ -z "$TOKEN" ]; then
    echo "Failed to generate token! Check logs:"
    docker logs quantum-api-container
    exit 1
fi
export TOKEN
echo "JWT Token: $TOKEN"

# --- Test app.py Endpoints (Port 5000) ---
echo "Testing app.py endpoints (port 5000)..."
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

# --- Test apiapp.py Endpoints (Port 7777) ---
echo "Testing apiapp.py endpoints (port 7777)..."
echo "1. /api/auth (token already generated)"
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

# --- Troubleshooting Tip ---
echo "If any test fails, check container logs with:"
echo "docker logs quantum-app-container"
echo "docker logs quantum-api-container"

echo "Testing complete!"