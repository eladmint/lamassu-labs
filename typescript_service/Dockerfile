# Multi-stage Dockerfile for Conference Commitment Service
# Security: Minimal Alpine Linux base with non-root user and restricted permissions

# Build stage
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache python3 make g++ protobuf protobuf-dev

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json tsconfig.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY src/ ./src/
COPY proto/ ./proto/

# Generate gRPC code and build TypeScript
RUN npm run proto:generate && npm run build

# Production stage
FROM node:18-alpine AS production

# Security: Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Install runtime dependencies only
RUN apk add --no-cache dumb-init

# Set working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json ./

# Security: Set restrictive permissions
RUN chmod -R 755 /app && \
    chmod -R 544 /app/dist

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "const grpc = require('@grpc/grpc-js'); \
                 const client = new grpc.Client('localhost:50051', grpc.credentials.createInsecure()); \
                 client.waitForReady(Date.now() + 5000, (err) => process.exit(err ? 1 : 0));"

# Expose gRPC port
EXPOSE 50051

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Start the service
CMD ["node", "dist/index.js"]

# Security labels
LABEL security.non-root="true" \
      security.network="restricted" \
      security.filesystem="readonly" \
      purpose="conference-commitment-protocol" \
      environment="base-sepolia-testnet-only"
