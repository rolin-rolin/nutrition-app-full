# Multi-stage build for optimized production image
# Build stage
FROM python:3.12-slim AS builder

# Set environment variables for build
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TORCH_CUDA_VERSION="cpu"
ENV CUDA_VISIBLE_DEVICES=""
ENV USE_CUDA="0"

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry for dependency management
RUN pip install poetry==1.7.1

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Export dependencies and install with pip
RUN set -e && \
    echo "Step 1: Exporting dependencies from Poetry..." && \
    poetry --version && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes --only main && \
    echo "Step 2: Installing dependencies with pip..." && \
    pip install --no-cache-dir -r requirements.txt

# Install CPU-only PyTorch
RUN set -e && \
    echo "Step 3: Installing CPU-only PyTorch..." && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Production stage
FROM python:3.12-slim

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TORCH_CUDA_VERSION="cpu"
ENV CUDA_VISIBLE_DEVICES=""
ENV USE_CUDA="0"

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy backend code and data
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p data

# Set proper permissions for data directory
RUN chmod -R 755 data/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start server with production settings
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
