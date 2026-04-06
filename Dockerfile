FROM python:3.12-slim

LABEL maintainer="fabiofilipe"
LABEL description="Crypto price collector with Discord alerts and web UI"

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/

# Create runtime dirs
RUN mkdir -p data logs

# Default: run scheduler
CMD ["python", "-m", "src.scheduler"]
