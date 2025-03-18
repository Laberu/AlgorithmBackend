# Project: Photogrammetry & Crack Detection System

## Overview
This project is a high-performance, scalable system designed for photogrammetry processing and automated crack detection on 3D models. The system efficiently processes large datasets of images using advanced algorithms while ensuring real-time job tracking and asynchronous execution. Built for reliability and scalability, it integrates Fastify (TypeScript), gRPC, Celery, Redis, PostgreSQL, and file-based storage solutions.

## Key Features
- Efficient Photogrammetry Processing: Handles large image datasets for 3D model reconstruction.
- Automated Crack Detection: Uses AI-based image analysis to identify structural cracks.
- High-Performance API Layer: Built with Fastify (TypeScript) for handling job submissions and tracking.
- Optimized Inter-Service Communication: Uses gRPC for fast data exchange between Fastify API and Python service.
- Asynchronous Processing: Celery ensures non-blocking, background execution of heavy computations.
- Job Status Tracking via File System: Python writes progress updates to `status.json` inside the job’s output directory.
- Persistent Data Storage: PostgreSQL keeps records of all job metadata and completion timestamps.
- Scalable File Management: Supports local storage or S3/MinIO for managing large-scale image and model outputs.
- Designed for Production: Supports Docker and Kubernetes for scalable deployments.

## System Architecture
```
/project
│── /backend-ts  (Fast API Layer - TypeScript)
│   │── /src
│   │   │── /grpc
│   │   │   ├── algorithm.proto  # gRPC contract for calling Python service
│   │   │   ├── client.ts        # Calls Python gRPC service
│   │   │── /api
│   │   │   ├── upload.ts        # Receives ZIP and starts job
│   │   │   ├── status.ts        # Reads `status.json` for job progress
│   │   │   ├── download.ts      # Fetches final ZIP file path from `status.json`
│   │   │   ├── health.ts        # Server health check endpoint
│   │── server.ts                # Fastify API entry point
│── /backend-py  (Algorithm Layer - Python)
│   │── photogrammetry.py        # Photogrammetry processing module
│   │── crack_detection.py       # AI-based crack detection module
│   │── grpc_server.py           # gRPC server for handling requests
│   │── background_worker.py     # Celery worker (async task execution)
│── /database
│   │── models.sql               # PostgreSQL schema for job metadata
│── /config
│   │── .env                     # Database settings and environment variables
│── /storage (or S3)
│   │── /job_12345/              # Output folder for job 12345
│   │   ├── status.json          # Real-time progress tracking written by Python
│   │   ├── final_output.zip     # Final processed ZIP file
│── Dockerfile                    # Deployment setup
│── README.md                     # Documentation
```

## Technologies Used
| Component | Technology |
|-----------|------------|
| API Layer | Fastify (TypeScript) |
| Inter-Service Communication | gRPC |
| Background Processing | Celery (Python) |
| Job Metadata Storage | PostgreSQL |
| Job Status Tracking | File System (`status.json`) |
| Machine Learning | TensorFlow/PyTorch (for crack detection) |
| File Storage | Local FS / S3 / MinIO |
| Deployment | Docker and Kubernetes |

## Workflow
1. **User uploads a ZIP file** containing images via Fastify API (`/api/upload`).
2. **Fastify records job details** in PostgreSQL and sends the ZIP to Python (via gRPC) along with an output directory path.
3. **Python extracts ZIP and starts processing** inside the output directory (`/storage/job_12345/`).
4. **Python writes job progress to `status.json`** inside the output directory.
5. **Fastify API checks job progress by reading `status.json`** when `/api/status/{job_id}` is called.
6. **Once processing is complete**, Python:
   - Generates a final ZIP file in the output directory.
   - Updates `status.json` with `"status": "completed"`.
7. **User requests `/api/download/{job_id}`** to retrieve the ZIP file path from `status.json`.
8. **Fastify serves the ZIP file to the user.**

## API Endpoints
| Method | Endpoint | Purpose |
|--------|---------|---------|
| GET | `/health` | Server health check |
| POST | `/api/upload` | Upload ZIP and start photogrammetry and crack detection |
| GET | `/api/status/{job_id}` | Read job progress from `status.json` |
| GET | `/api/download/{job_id}` | Retrieve final ZIP file path from `status.json` |

## Getting Started
### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/photogrammetry-crack-detection.git
cd photogrammetry-crack-detection
```

### 2. Setup Environment Variables
Create a `.env` file:
```
POSTGRES_URL=postgres://user:password@localhost:5432/jobs_db
S3_BUCKET_NAME=my-image-bucket
```

### 3. Install Dependencies
#### Backend (Fastify - TypeScript)
```sh
cd backend-ts
npm install
```

#### Backend (Python - Processing Services)
```sh
cd backend-py
pip install -r requirements.txt
```

### 4. Run the Services
#### Start PostgreSQL (Using Docker)
```sh
docker-compose up -d
```

#### Start Fastify API
```sh
cd backend-ts
npm run dev
```

#### Start Python gRPC Server and Celery Worker
```sh
cd backend-py
python grpc_server.py & celery -A background_worker worker --loglevel=info
```

### 5. Test API
```sh
# Check server status
curl -X GET http://localhost:3000/health

# Upload a ZIP file
curl -X POST -F 'file=@images.zip' http://localhost:3000/api/upload

# Check job status
curl -X GET http://localhost:3000/api/status/12345

# Download final ZIP file
curl -X GET http://localhost:3000/api/download/12345
```

## Future Enhancements
- Implement distributed processing to handle large photogrammetry tasks faster.
- Enhance AI-based crack detection models with deep learning improvements.
- Optimize Kubernetes auto-scaling to dynamically allocate resources.
- Integrate WebSocket support for real-time UI updates.

## License
This project is licensed under the MIT License.

#   A l g o r i t h m B a c k e n d  
 