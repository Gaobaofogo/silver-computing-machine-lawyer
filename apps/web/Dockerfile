# # stage 1: build
# FROM node:20-alpine AS builder
# WORKDIR /app
# COPY package.json .
# RUN npm install
# COPY . .
# RUN npm run build

# # stage 2: serve (development)
# FROM node:20-alpine
# WORKDIR /app
# COPY --from=builder /app /app
# EXPOSE 5173
# CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm i

COPY . .


# FROM base AS dev

# RUN npm install -g @vtsls/language-server typescript

EXPOSE 3000
CMD ["npm", "run", "dev"]


# FROM base AS prod

# RUN npm run build
# EXPOSE 3000
# CMD ["npx", "serve", "-s", "dist", "-l", "3000"]