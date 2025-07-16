# Treasury Monitor Agent - Enterprise Dockerfile
# Following tokenhunter-457310 enterprise deployment patterns

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from project root (enterprise standard)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Treasury Monitor agent implementation (PRIVATE/PREMIUM)
COPY agent_forge/examples/premium/treasury_monitor_agent.py ./treasury_monitor_agent.py

# Copy web server wrapper
COPY src/treasury_monitor/web_server.py ./web_server.py

# Copy Agent Forge framework core
COPY agent_forge/src/ ./agent_forge_src/

# Copy necessary framework components
COPY src/shared/ ./src/shared/

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/config

# Set environment variables for enterprise deployment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DEPLOYMENT_ENV=production

# Expose port for Cloud Run
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start Treasury Monitor web server
CMD ["python", "web_server.py"]
