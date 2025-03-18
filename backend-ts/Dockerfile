# Use official Node image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Ensure TypeScript is installed globally
RUN npm install -g typescript

# Copy all source code
COPY . .

# Create dist directory for gRPC proto files
RUN mkdir -p dist/grpc

# Copy proto file
COPY src/grpc/algorithm.proto dist/grpc/algorithm.proto

# Ensure TypeScript is available
RUN npx tsc -v  # ✅ This checks if TypeScript is installed

# Build the project
RUN npm run build  # ✅ This compiles TypeScript

# Expose port
EXPOSE 4000

# Start the server
CMD ["node", "dist/server.js"]
