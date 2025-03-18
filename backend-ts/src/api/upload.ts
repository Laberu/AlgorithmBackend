import { FastifyInstance, FastifyRequest } from "fastify";
import fs from "fs";
import path from "path";
import { streamFileToPython } from "../grpc/client";
import { MultipartFile } from "@fastify/multipart";

export default async function uploadRoutes(fastify: FastifyInstance) {
    fastify.post("/api/upload", async (request: FastifyRequest, reply) => {
        try {
            // ✅ Log request headers for debugging
            console.log("🔍 Request Headers:", request.headers);

            // ✅ Ensure request is multipart
            if (!request.isMultipart()) {
                return reply.status(400).send({ error: "Request is not multipart" });
            }

            // ✅ Get file from request
            const data: MultipartFile | undefined = await request.file();
            if (!data) {
                return reply.status(400).send({ error: "No file uploaded" });
            }

            // Generate job ID
            const jobId = Date.now().toString();

            // Define temp directory
            const tempDir = path.join(__dirname, "../../temp");
            const tempPath = path.join(tempDir, `${jobId}.zip`);

            // ✅ Ensure the temp directory exists
            if (!fs.existsSync(tempDir)) {
                fs.mkdirSync(tempDir, { recursive: true });
            }

            // Save file to temp directory
            await new Promise<void>((resolve, reject) => {
                const fileStream = fs.createWriteStream(tempPath);
                data.file.pipe(fileStream);
                fileStream.on("finish", () => resolve());
                fileStream.on("error", (err: NodeJS.ErrnoException) => reject(err));
            });

            console.log(`✅ File temporarily saved: ${tempPath}`);

            // Stream file to Python via gRPC
            const response = await streamFileToPython(jobId, tempPath);
            console.log("🔄 gRPC Response:", response);

            // Delete temp file after streaming
            fs.unlinkSync(tempPath);

            return reply.status(201).send({
                job_id: jobId,
                grpc_status: response.status,
            });

        } catch (error) {
            console.error("❌ Upload Error:", error);
            return reply.status(500).send({ error: "Upload failed" });
        }
    });
}
