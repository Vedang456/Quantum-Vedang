# Dockerfile for app.py
FROM bitnami/tensorflow:2.18.0


WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what's needed for app.py
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Run app.py
CMD ["sleep", "1000"]
#CMD ["/opt/bitnami/python/bin/python3", "/app/app.py"]
