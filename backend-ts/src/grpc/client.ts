import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import path from "path";
import fs from "fs";
import dotenv from "dotenv";

// ✅ Load environment variables
dotenv.config();

const PROTO_PATH = path.join(__dirname, "algorithm.proto");
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});
const grpcObject = grpc.loadPackageDefinition(packageDefinition);
const AlgorithmProto = grpcObject.algorithm as any;

// ✅ Use environment variable for gRPC server address
const GRPC_HOST = process.env.GRPC_HOST || "backend-py:50051";

// ✅ Create gRPC client
const client = new AlgorithmProto.AlgorithmService(
    GRPC_HOST,
    grpc.credentials.createInsecure()
);

/**
 * Streams a file to backend-py via gRPC
 * @param jobId Unique job identifier
 * @param filePath Path to the uploaded file
 */
export function streamFileToPython(jobId: string, filePath: string): Promise<any> {
    return new Promise((resolve, reject) => {
        const stream = client.UploadFile((error: any, response: any) => {
            if (error) {
                console.error("gRPC Upload Error:", error);
                return reject(error);
            }
            console.log("gRPC Upload Success:", response);
            resolve(response);
        });

        // Read file in chunks and send via gRPC
        const fileStream = fs.createReadStream(filePath);
        fileStream.on("data", (chunk) => {
            stream.write({ job_id: jobId, content: chunk });
        });

        fileStream.on("end", () => {
            stream.end();
        });

        fileStream.on("error", (err) => {
            reject(err);
        });
    });
}

/**
 * Fetches job status from backend-py via gRPC
 * @param jobId Unique job identifier
 */
export function getJobStatus(jobId: string): Promise<any> {
    return new Promise((resolve, reject) => {
        client.GetJobStatus({ job_id: jobId }, (error: any, response: any) => {
            if (error) {
                console.error("gRPC Error:", error);
                reject(error);
            } else {
                console.log("gRPC Response:", response);
                resolve(response);
            }
        });
    });
}

export async function getFileFromPython(jobId: string): Promise<Buffer | null> {
    return new Promise((resolve, reject) => {
        const call = client.DownloadFile({ job_id: jobId });

        let fileBuffer: Buffer[] = [];

        call.on("data", (chunk: { content: Buffer }) => { // ✅ Explicitly type `chunk`
            fileBuffer.push(chunk.content);
        });

        call.on("end", () => {
            console.log(`✅ File for job ${jobId} received from backend-py`);
            resolve(Buffer.concat(fileBuffer));
        });

        call.on("error", (err: Error) => { // ✅ Explicitly type `err`
            console.error("❌ Error downloading file:", err);
            reject(null);
        });
    });
}

export async function confirmDelete(jobId: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
        client.ConfirmDelete({ job_id: jobId }, (err: Error | null, response: { success: boolean }) => {
            if (err) {
                console.error("❌ Cleanup Error:", err);
                return reject(false);
            }
            console.log(`🗑️ Cleanup confirmed for job ${jobId}`);
            resolve(response.success);
        });
    });
}
