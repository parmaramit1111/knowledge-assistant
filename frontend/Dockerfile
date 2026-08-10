# =========================
# Build Stage
# =========================

FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY package*.json ./

RUN npm ci

# Copy frontend source
COPY . .

# Build production bundle
RUN npm run build


# =========================
# Production Stage
# =========================

FROM nginx:1.29-alpine

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy our nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy Vite production build
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]