.PHONY: keycloak example-service up down

keycloak:
	docker-compose up -d

example-service:
	docker-compose -f src/example_service/docker-compose.yml up -d

up: keycloak example-service

down:
	docker-compose -f src/example_service/docker-compose.yml down
	docker-compose down
