# Use official Python image (matching your pyproject.toml requirement)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Force CPU-only versions for ML libraries
ENV TORCH_CUDA_VERSION="cpu"
ENV CUDA_VISIBLE_DEVICES=""
ENV USE_CUDA="0"

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry for dependency management
# Poetry provides better dependency resolution and uses poetry.lock for exact versions
RUN pip install poetry

# Configure Poetry to not create virtual environment in container
RUN poetry config virtualenvs.create false

# Copy Poetry files first for better Docker layer caching
# poetry.lock contains the exact versions that work together locally
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
# This will use the exact versions from poetry.lock for reproducible builds
# --no-dev excludes development dependencies like pytest
RUN set -e && \
    echo "Installing dependencies with Poetry..." && \
    poetry install --no-dev --no-interaction --no-ansi && \
    echo "Installing CPU-only PyTorch..." && \
    poetry run pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    echo "All dependencies installed successfully!"

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

# Start server with production settings using Poetry
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
