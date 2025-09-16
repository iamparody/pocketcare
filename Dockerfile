# Use lightweight Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Initialize Reflex (build frontend assets)
RUN reflex init

# Expose only port 8000 for Render
EXPOSE 8000

# Run Reflex backend-only in production mode
CMD ["reflex", "run", "--env", "prod", "--backend-only", "--backend-host", "0.0.0.0", "--backend-port", "8000"]
