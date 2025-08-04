# Multi-stage Dockerfile optimized for Agent Forge deployment
FROM python:3.11-slim as builder

# Build stage - compile dependencies
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Agent Forge branding and metadata
LABEL maintainer="Agent Forge State Generator Team"
LABEL description="AI-powered workflow state generator for Agent Forge platform"
LABEL version="1.0.0"
LABEL platform="agent-forge"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create non-root user for security (Agent Forge best practices)
RUN useradd -m -u 1000 agentforge && \
    chown -R agentforge:agentforge /app && \
    chmod +x /app/scripts/generate_agent_forge_data.py

# Switch to non-root user
USER agentforge

# Health check for Agent Forge monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Expose port
EXPOSE 8000

# Environment variables for Agent Forge
ENV PYTHONPATH=/app
ENV AGENT_FORGE_MODE=production
ENV LOG_LEVEL=INFO

# Start with Agent Forge optimized settings
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--access-log"]
