FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Serve with nginx
FROM nginx:stable-alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html

# Remove default nginx config & use custom if needed
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
