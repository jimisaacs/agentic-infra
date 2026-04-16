# Stack (Docker Compose)

The worked-example app runs as a multi-service Docker Compose stack under `project/stack/`. Containers are the default way to run and verify (P14).

## Service architecture

```
compose.yml
  go-app     Go HTTP server (port 8080)
  web        nginx serving React build + API proxy (port 3000)

nginx.conf
  /api/*     → proxy to go-app:8080
  /*         → serve static React build, SPA fallback
```

The web service depends on go-app. Build context is `project/` so Dockerfiles can access both `go/` and `web/` source.

## Control plane

All stack operations go through `./dev` (see `cli` rule):

- `./dev stack up` -- build and start
- `./dev stack down` -- stop
- `./dev stack logs` -- stream logs
- `./dev stack status` -- show containers
- `./dev stack dev` -- host-native dev servers (requires local Go + Node)
- `./dev verify` -- includes Docker-based web build check (P15)

## Anti-patterns

- Don't bypass `./dev stack` with raw `docker compose`
- Don't hardcode service hostnames in application code
- Don't add build steps that require host-local toolchains
- Don't add ports that conflict with defaults (3000, 5173, 8080)
