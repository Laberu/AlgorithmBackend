# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy dependencies first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Expose gRPC port
EXPOSE 50051

# Run gRPC server
CMD ["uvicorn", "rest_server:app", "--host", "0.0.0.0", "--port", "50051"]
