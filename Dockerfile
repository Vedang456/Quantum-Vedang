# Dockerfile for app.py
FROM tensorflow/tensorflow:latest

WORKDIR /app

# Copy requirements and handle blinker with --ignore-installed
COPY requirements.txt .
RUN pip install --no-cache-dir --ignore-installed blinker==1.8.2 && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy only what's needed for app.py
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Run app.py using the base image's Python
CMD ["/usr/bin/python3", "/app/app.py"]