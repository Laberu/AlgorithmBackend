# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy dependencies first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the .proto file (AFTER MOVING IT TO backend-py)
COPY algorithm.proto /app/

# ✅ Generate gRPC Python files
RUN python -m grpc_tools.protoc -I/app --python_out=/app --grpc_python_out=/app /app/algorithm.proto

# Copy the rest of the files
COPY . .

# Expose gRPC port
EXPOSE 50051

# Run gRPC server
CMD ["uvicorn", "rest_server:app", "--host", "0.0.0.0", "--port", "50051"]
