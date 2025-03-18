import { FastifyInstance, FastifyRequest } from "fastify";
import { getJobStatus } from "../grpc/client";

export default async function statusRoutes(fastify: FastifyInstance) {
    fastify.get("/api/status/:jobId", async (request: FastifyRequest<{ Params: { jobId: string } }>, reply) => {
        try {
            const { jobId } = request.params;
            const status = await getJobStatus(jobId);

            if (status.status === "not_found") {
                return reply.status(404).send({ error: status.message });
            }

            return reply.status(200).send(status);
        } catch (error) {
            console.error("❌ Status Check Error:", error);
            return reply.status(500).send({ error: "Failed to retrieve job status." });
        }
    });
}
