FROM node:22-alpine

WORKDIR /app
COPY web/package.json web/package-lock.json* ./
RUN --mount=type=cache,target=/root/.npm \
    npm install
COPY web/ .

RUN npx tsc --noEmit

CMD ["npx", "vite", "build", "--watch", "--outDir", "/dist"]
