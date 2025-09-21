# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 7860

# Health check
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]