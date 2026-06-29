FROM python:3.10-slim

WORKDIR /app

# Upgrade pip and set longer timeouts
RUN pip install --no-cache-dir --upgrade pip && \
    pip config set global.timeout 1000

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies with extended timeouts and retries
RUN pip install --no-cache-dir --default-timeout=1000 --retries=5 -r requirements.txt

# Pre-download the embedding model (also with timeout)
RUN python -c "import os; os.environ['HF_HUB_ENABLE_HF_TRANSFER']='1'; from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Copy application code
COPY ./app ./app
COPY ./scripts ./scripts

# Set Python path
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]