# Stage 1: Base Bun image
FROM oven/bun:1.0.31-alpine AS builder

WORKDIR /app

# Install dependencies
COPY bun.lock /app/bun.lock
COPY package.json /app/package.json
RUN bun install

# Copy the rest of the files
COPY . .

# Optional: Precompile TypeScript if needed
RUN bun build index.ts --outdir=dist --target=node

# Stage 2: Lightweight production image
FROM oven/bun:1.0.31-alpine

WORKDIR /app

# Copy only built files & dependencies
COPY --from=builder /app/bun.lockb ./
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

EXPOSE 3000

# Run the built JS (or replace with `bun src/index.ts` if running TS directly)
CMD ["bun", "dist/index.js"]
