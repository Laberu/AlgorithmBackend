import Fastify from "fastify";
import fastifyMultipart from "@fastify/multipart";
import dotenv from "dotenv";
import fastifyMetrics from "fastify-metrics";

import healthRoutes from "./api/health";
import uploadRoutes from "./api/upload";
import statusRoutes from "./api/status";
import downloadRoutes from "./api/download";

// ✅ Load environment variables
dotenv.config();

const PORT = process.env.PORT || 3000; // ✅ Use env variable for port

const fastify = Fastify({ logger: true });

// ✅ Register multipart support (for file uploads)
fastify.register(fastifyMultipart);

// ✅ Register routes
fastify.register(healthRoutes);
fastify.register(uploadRoutes);
fastify.register(statusRoutes);
fastify.register(downloadRoutes);

// ✅ Enable Prometheus Metrics on `/metrics`
fastify.register(fastifyMetrics, { endpoint: "/metrics" });

// ✅ Start server using the environment variable
fastify.listen({ port: 3000, host: "0.0.0.0" }, (err, address) => {
    if (err) {
        fastify.log.error(err);
        process.exit(1);
    }
    console.log(`🚀 Server running at ${address}`);
});
