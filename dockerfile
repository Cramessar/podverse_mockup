# 1. Use official Node.js LTS image as builder
FROM node:18-alpine AS builder

# 2. Set working directory
WORKDIR /app

# 3. Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# 4. Install dependencies (with package lock)
RUN npm install

# 5. Copy the rest of your app's source code
COPY . .

# 6. Build the Next.js app
RUN npm run build

# 7. Remove dev dependencies to keep image slim
RUN npm prune --production

# 8. Production image using smaller Node.js Alpine image
FROM node:18-alpine AS runner

WORKDIR /app

# 9. Copy built files and prod deps from builder stage
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# 10. Expose port 3000 (default Next.js)
EXPOSE 3000

# 11. Start the Next.js app in production mode
CMD ["npm", "start"]
