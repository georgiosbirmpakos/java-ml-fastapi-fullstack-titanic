# ML Model Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ML model source code
COPY . .

# Create models directory
RUN mkdir -p models

# Download data and train model
RUN python download_data.py && python train.py

# Expose port (if needed for serving)
EXPOSE 8001

# Default command
CMD ["python", "predict.py"]
