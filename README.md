# Quantum Intelligence API

This project provides two Flask-based applications: `quantum-app` (port 5000) and `quantum-api` (port 7777), containerized with Docker for local development and deployment to Kubernetes. This README summarizes the setup and steps taken to push Docker images to Docker Hub, up to the point before Kubernetes deployment.

---

## Prerequisites

- **Operating System**: Linux (e.g., Pop!_OS, Ubuntu), macOS, or Windows with WSL2.
- **Docker**: Installed and running (`docker --version` to check).
- **curl**: For testing endpoints (`curl --version` to check).
- **Minikube**: For local Kubernetes testing (optional, installed later).
- **Terminal**: Access to a command-line interface.

---

## Project Structure

- **Dockerfiles**:
  - `Dockerfile`: For `quantum-app` (port 5000, `app.py`).
  - `Dockerfile.api`: For `quantum-api` (port 7777, `api/apiapp.py`).
- **Dependencies**: `requirements.txt` lists Python dependencies (e.g., TensorFlow, Flask, blinker).
- **Scripts**: `test.sh` for testing endpoints.
- **Source Code**: Restricted; work with pre-built Docker images or provided package.

---

## Steps Taken

### 1. Initial Setup
- Navigated to `~/Desktop/Quantum-1/Quantum-Vedang`.
- Installed Docker, Python dependencies via `pip install -r requirements.txt`, and resolved TensorFlow compatibility issues.

### 2. Dockerfile Development
- Created Dockerfiles using `tensorflow/tensorflow:latest`, fixing:
  - `blinker` uninstallation errors with `--ignore-installed` and `--break-system-packages`.
  - Bash installation for debugging with `apt-get install -y bash` (root privileges).
  - `apt-get` errors (e.g., missing `/var/lib/apt/lists/partial`) by initializing directories.
  - Removed virtual environments for simplicity, using base image Python directly.

### 3. Building and Running Containers
- Built images: `docker build -t quantum-app:latest -f Dockerfile .` and `docker build -t quantum-api:latest -f Dockerfile.api .`.
- Ran containers locally: `docker run -d -p 5000:5000 --name quantum-app-container quantum-app:latest` and `docker run -d -p 7777:7777 --name quantum-api-container quantum-api:latest`.
- Debugged issues like `SyntaxError` (null bytes) by verifying files, paths, and `CMD`.

### 4. Testing Endpoints
- Used `test.sh` or `curl` to test all endpoints, ensuring `"status": "success"` for:
  - `quantum-app`: `/generate_entropy`, `/encrypt`, `/decrypt`, `/predict`.
  - `quantum-api`: `/api/auth`, `/api/process-signal`, `/api/detect-anomalies`, `/api/encrypt`, `/api/quantum-intelligence`, `/api/metrics`.

### 5. Docker Desktop and Resource Issues
- Fixed Docker Desktop resource misconfigurations (0 CPUs/0B memory) by allocating 2 CPUs and 4GB memory in settings.
- Resolved VS Code Docker extension authentication errors (401 Unauthorized) by logging into Docker Hub with `docker login`.

### 6. Pushing to Docker Hub
- Tagged images: `docker tag quantum-app:latest vedanglimaye/quantum-app:latest` and `docker tag quantum-api:latest vedanglimaye/quantum-api:latest`.
- Pushed to Docker Hub: `docker push vedanglimaye/quantum-app:latest` and `docker push vedanglimaye/quantum-api:latest`.
- Confirmed success via Docker Hub UI and terminal output.

---

## Current State
- Docker images `quantum-app:latest` and `quantum-api:latest` are successfully pushed to Docker Hub under `vedanglimaye/quantum-app` and `vedanglimaye/quantum-api`.
- Local containers are running, and endpoints are functional.
- Ready for Kubernetes deployment using Minikube or a cloud provider.

---

## Next Steps
- **Deploy to Kubernetes**: Update `app-deployment.yaml` and `api-deployment.yaml` with `vedanglimaye/quantum-app:latest` and `vedanglimaye/quantum-api:latest`, then apply with `kubectl apply -f ...`.
- **Test in Kubernetes**: Use Minikube service URLs to test endpoints via `curl`.
- **Optimize**: Consider multi-stage Dockerfiles to reduce image size or add resource limits for stability.

---

## Troubleshooting
- **Build Failures**: Check `docker build` logs for `pip` or `apt-get` errors; use `--no-cache` to rebuild.
- **Container Issues**: Use `docker logs <container-name>` or `docker run -it <image-name> /bin/bash` for debugging.
- **Docker Hub Push**: Ensure `docker login` works; verify repositories on [hub.docker.com/u/vedanglimaye](https://hub.docker.com/u/vedanglimaye).

---

## Support
Report issues to [insert contact/support channel].

Enjoy using the Quantum Intelligence API!


### Notes on Security and Source Code Protection
- **No Source Code Exposure**: The README avoids mentioning Python files or implementation details, focusing on Docker images and `curl` commands.
- **Distribution Options**:
  - **Pre-built Images**: Push `quantum-app:latest` and `quantum-api:latest` to a private Docker Hub repository or a cloud registry (e.g., AWS ECR) and provide pull instructions with credentials.
    ```bash
    docker push yourusername/quantum-app:latest
    docker push yourusername/quantum-api:latest
Package: Zip the directory without Python files (Dockerfile, Dockerfile.api, requirements.txt, setup_and_test.sh), or provide a tarball with binaries if compiled.
Token Handling: Users generate their own JWT via /api/auth, keeping authentication secure.