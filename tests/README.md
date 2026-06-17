# Testing

## Postman collection (via Newman)

### Production Environment

Tests can be run against the production server.

```bash
newman run ./tests/tracks-api.postman_collection.json -e ./tests/prod-env.postman_environment.json
```

### Local testing

Using docker

```bash
docker compose up -d

newman run ./tests/tracks-api.postman_collection.json -e ./tests/docker-env.postman_environment.json
```
