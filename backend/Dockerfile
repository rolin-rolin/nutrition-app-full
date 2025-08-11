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

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies in specific order for compatibility
# This order ensures NumPy 2.0.0 is installed first, then PyTorch CPU-only versions,
# then sentence-transformers and other dependencies that depend on them
RUN pip install --no-cache-dir --upgrade pip && \
    # Install NumPy first to ensure compatibility
    pip install --no-cache-dir "numpy==2.0.0" && \
    # Install CPU-only PyTorch
    pip install --no-cache-dir --find-links https://download.pytorch.org/whl/torch_stable.html \
        torch==2.1.0+cpu \
        torchvision==0.16.0+cpu \
        torchaudio==2.1.0+cpu && \
    # Install remaining dependencies
    pip install --no-cache-dir -r requirements.txt

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
