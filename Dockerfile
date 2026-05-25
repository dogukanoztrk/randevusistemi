# ============================================
# Stage 1: Build the Vue.js frontend
# ============================================
FROM node:22-slim AS build-stage

WORKDIR /app

# Copy package files first for better Docker layer caching
COPY package*.json ./
RUN npm ci --silent

# Copy project files and build
COPY . .
RUN npm run build

# ============================================
# Stage 2: Serve with Nginx
# ============================================
FROM nginx:alpine AS production-stage

# Copy the built files from the build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy the custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Healthcheck to verify nginx is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
