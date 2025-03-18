import { FastifyInstance } from "fastify";
import os from "os";

export default async function healthRoutes(fastify: FastifyInstance) {
    fastify.get("/health", async (request, reply) => {
        return reply.send({
            status: "ok",
            uptime: process.uptime(),
            server: os.hostname(),
            timestamp: new Date().toISOString(),
        });
    });
}
