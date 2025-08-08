# Keycloak Auth Service Example

This repository provides a minimal example of running a Keycloak identity server and a Python/Django REST Framework (DRF) service that uses Keycloak for authentication. It can serve as a starting point for integrating Keycloak as the auth-service in your microservices ecosystem.

## Contents

- `docker-compose.yml` – launches a Keycloak server in development mode.
- `keycloak-realm.json` – realm export defining demo entities.
- `src/example_service/` – simple DRF service with Keycloak-based JWT authentication.
- `requirements.txt` – Python dependencies.

## Prerequisites

- Docker and Docker Compose
- Python 3.11+

## Running Keycloak

To start only the Keycloak server:

```bash
make keycloak
```

Keycloak will be available at `http://localhost:8080` with admin credentials `admin/admin`.
The imported realm `demo` contains:
   - confidential client `demo-client` with secret `demo-secret`
   - realm role `user`
   - user `alice` with password `alice` and role `user`

## Running the DRF service

Start the example service with its Docker Compose file:

```bash
docker-compose -f src/example_service/docker-compose.yml up
```

The API will be available at `http://localhost:8000/api/`.

Verify the service is running:

```bash
curl http://localhost:8000/api/healthz/
```

which should return `{ "ping": "pong" }`.

To run both Keycloak and the example service at once, use:

```bash
make up
```

Stop both with:

```bash
make down
```

### Obtaining a token

Use the demo user to obtain an access token from Keycloak:

```bash
curl -X POST \
  http://localhost:8080/realms/demo/protocol/openid-connect/token \
  -d "client_id=demo-client" \
  -d "client_secret=demo-secret" \
  -d "grant_type=password" \
  -d "username=alice" \
  -d "password=alice"
```

The response contains `access_token` that your microservices can include in the
`Authorization` header when calling protected endpoints.

## Keycloak entities overview

- **Realm**: `demo`
- **Client**: `demo-client` (confidential, uses client secret)
- **Role**: `user`
- **User**: `alice` (assigned `user` role)

## Environment variables for services

The DRF service uses the following environment variables to connect to Keycloak:

- `KEYCLOAK_SERVER_URL` (default `http://localhost:8080/`)
- `KEYCLOAK_REALM` (default `demo`)
- `KEYCLOAK_CLIENT_ID` (default `demo-client`)
- `KEYCLOAK_CLIENT_SECRET` (default empty)

Each microservice can use the same authentication class from `src/example_service/example_service/api/authentication.py` or adapt it to its needs.

## Tests

Run the Django test suite:

```bash
python src/example_service/manage.py test example_service.api
```
