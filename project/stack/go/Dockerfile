FROM golang:1.23-alpine AS build

WORKDIR /src

COPY go/app/go.mod go/app/go.sum* go/app/
COPY go/shared/go.mod go/shared/

WORKDIR /src/go/app
RUN go mod download

WORKDIR /src
COPY go/shared/ go/shared/
COPY go/app/    go/app/

WORKDIR /src/go/app
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -ldflags="-s -w" -o /pulse-app .

FROM alpine:3.21

RUN adduser -D -u 1001 appuser
COPY --from=build /pulse-app /usr/local/bin/pulse-app
USER appuser
EXPOSE 8080
CMD ["pulse-app"]
