import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { getFileFromPython, confirmDelete } from "../grpc/client";

export default async function downloadRoutes(fastify: FastifyInstance) {
    fastify.get("/api/download/:jobId", async (request: FastifyRequest<{ Params: { jobId: string } }>, reply: FastifyReply) => {
        try {
            const { jobId } = request.params;

            const fileBuffer = await getFileFromPython(jobId);
            if (!fileBuffer) {
                return reply.status(404).send({ error: "File not found or job not completed yet." });
            }

            // ✅ Send file to client
            reply.header("Content-Type", "application/zip");
            reply.header("Content-Disposition", `attachment; filename="${jobId}.zip"`);
            reply.send(fileBuffer);

            // ✅ After successful download, confirm cleanup
            confirmDelete(jobId).catch(console.error); // Don't block the response, run in the background

        } catch (error) {
            console.error("❌ Download Error:", error);
            return reply.status(500).send({ error: "Failed to download file." });
        }
    });
}
