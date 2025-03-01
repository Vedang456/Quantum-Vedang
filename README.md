# Quantum Intelligence API

This project provides two Flask-based applications: a lightweight quantum-inspired API (`app.py`) and a comprehensive quantum intelligence API (`apiapp.py`). These applications are containerized using Docker for easy deployment and testing. This README guides you through setting up, running, and testing the APIs locally.

**Note**: This guide is for end-users. Source code access is restricted; you’ll work with pre-built Docker images or a provided package.

---

## Prerequisites

- **Operating System**: Linux (e.g., Ubuntu, Pop!_OS), macOS, or Windows with WSL2.
- **Docker**: Installed and running (`docker --version` to check).
- **curl**: For testing endpoints (`curl --version` to check).
- **Terminal**: Access to a command-line interface.

---

## Project Structure

The project includes:
- Two Docker images: `quantum-app` (port 5000) and `quantum-api` (port 7777).
- Configuration files: `Dockerfile`, `Dockerfile.api`, `requirements.txt`.
- A test script: `setup_and_test.sh`.

You’ll receive a package with these files but not the source code.

---

## Setup Instructions

### 1. Obtain the Project Package

- **Option 1**: Download the pre-packaged ZIP file from [insert secure link/source].
- **Option 2**: Pull pre-built Docker images from a private registry (e.g., Docker Hub):
  docker pull your-registry/quantum-app:latest
  docker pull your-registry/quantum-api:latest
Replace your-registry with the provided registry path (e.g., yourusername).

# 2. Navigate to the Project Directory

Unzip the package (if applicable):


unzip quantum_project.zip -d ~/Desktop/Quantum-1/Quantum-Vedang
cd ~/Desktop/Quantum-1/Quantum-Vedang

## Or, if using pre-built images, proceed directly to Step 4.

# 3. Install Dependencies and Build Docker Images

Install System Dependencies (Linux):

sudo apt update
sudo apt install -y python3-dev python3-pip libatlas-base-dev
Install Python Dependencies (if building locally):

pip install -r requirements.txt
Build Docker Images (skip if using pre-built images):
\
docker build -t quantum-app:latest -f Dockerfile .
docker build -t quantum-api:latest -f Dockerfile.api .



# 4. Run the Docker Containers

Start quantum-app (port 5000):

docker run -d -p 5000:5000 --name quantum-app-container quantum-app:latest
Start quantum-api (port 7777):

docker run -d -p 7777:7777 --name quantum-api-container quantum-api:latest
Verify:

docker ps -a
Look for quantum-app-container and quantum-api-container with status "Up".


# Testing the APIs

Automated Testing Script
Use the provided setup_and_test.sh to automate setup and testing:

chmod +x setup_and_test.sh
./setup_and_test.sh

This script:

Installs dependencies (if needed).
Builds and runs Docker images.
Tests all endpoints and prints results.
Manual Testing with curl
app.py (Port 5000)
No authentication required.
# /generate_entropy:

curl -k "https://localhost:5000/generate_entropy?seed=42"

# /encrypt:

curl -k -X POST -H "Content-Type: application/json" -d '{"data": "hello"}' https://localhost:5000/encrypt

# /decrypt:

curl -k -X POST -H "Content-Type: application/json" -d '{"encrypted_data": "<encrypted_data>"}' https://localhost:5000/decrypt
Replace <encrypted_data> with the output from above.


# /predict:

curl -k -X POST -H "Content-Type: application/json" -d '{"value": 42}' https://localhost:5000/predict



# apiapp.py (Port 7777)
# Requires a JWT token for most endpoints.
# Generate Token (/api/auth):

curl -k -X POST -H "Content-Type: application/json" -d '{"api_key": "test-key"}' https://localhost:7777/api/auth


# Set token:

export TOKEN="your-token-here"


# /api/process-signal:

curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"signal_data": [1, 2, 3, 4, 5]}' https://localhost:7777/api/process-signal


# /api/detect-anomalies:

curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"data": [1, 2, 3, 4, 5], "threshold": 0.8}' https://localhost:7777/api/detect-anomalies


# /api/encrypt:

curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"data": "secret"}' https://localhost:7777/api/encrypt


# /api/quantum-intelligence:

curl -k -X POST -H "Content-Type: application/json" -H "X-API-Key: $TOKEN" -d '{"data_stream": [1, 2, 3, 4, 5]}' https://localhost:7777/api/quantum-intelligence

# /api/metrics:

curl -k -H "X-API-Key: $TOKEN" https://localhost:7777/api/metrics



# Troubleshooting
# 1.Container Not Running:

docker logs quantum-app-container
docker logs quantum-api-container

# 2.Port Conflict:
Stop conflicting processes or change ports (e.g., -p 5001:5000).

# 3.Empty Reply:
Ensure HTTPS with -k, check logs for startup errors.


# Next Steps

Validate Outputs: Run all tests and ensure "status": "success".
Deployment: Contact the project owner for Kubernetes setup instructions using pre-built images.
Support: Report issues to [insert contact/support channel].
Enjoy exploring the Quantum Intelligence API!


---

### Notes on Security and Source Code Protection
- **No Source Code Exposure**: The README avoids mentioning Python files or implementation details, focusing on Docker images and `curl` commands.
- **Distribution Options**:
  - **Pre-built Images**: Push `quantum-app:latest` and `quantum-api:latest` to a private Docker Hub repository or a cloud registry (e.g., AWS ECR) and provide pull instructions with credentials.
    ```bash
    docker push yourusername/quantum-app:latest
    docker push yourusername/quantum-api:latest
Package: Zip the directory without Python files (Dockerfile, Dockerfile.api, requirements.txt, setup_and_test.sh), or provide a tarball with binaries if compiled.
Token Handling: Users generate their own JWT via /api/auth, keeping authentication secure.