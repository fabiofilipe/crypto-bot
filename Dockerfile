FROM python:3.12-slim

LABEL maintainer="fabiofilipe"
LABEL description="Crypto price collector with Discord alerts and PostgreSQL"

WORKDIR /app

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source
COPY src/ ./src/

# Runtime dirs
RUN mkdir -p data logs

CMD ["python", "-m", "src.scheduler"]
