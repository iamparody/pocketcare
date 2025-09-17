# Base image
FROM python:3.11-slim

# Install system dependencies (Node.js + Nginx)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    nodejs \
    npm \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Build frontend
RUN reflex init
RUN reflex export --frontend-only --no-zip -o /app/web_build

# Add Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Environment
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose only one port
EXPOSE 8080

# Start backend + Nginx in foreground
CMD sh -c "reflex run --env prod --backend-host 0.0.0.0 --backend-port 8000 & nginx -g 'daemon off;'"
