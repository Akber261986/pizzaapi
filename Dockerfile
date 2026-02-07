# Dockerfile - Version 1 (with UV)

FROM python:3.13 
WORKDIR /app

# Install UV
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies with UV (much faster!)
RUN uv sync --frozen --no-dev

# Copy application code
COPY main.py .

EXPOSE 7860

# Run with UV
CMD ["uv", "run", "main.py"]
