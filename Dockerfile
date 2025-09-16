# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Reflex
RUN pip install --no-cache-dir reflex

# Copy app files
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run Reflex in production mode
CMD ["reflex", "run", "--env", "prod", "--host", "0.0.0.0", "--port", "10000"]
