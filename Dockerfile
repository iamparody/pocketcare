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

# Expose the port dynamically (Render uses $PORT)
EXPOSE $PORT

# Run Reflex in production mode, binding to Render's port
CMD ["sh", "-c", "reflex run --env prod --backend-host 0.0.0.0 --backend-port $PORT"]
