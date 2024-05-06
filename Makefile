.PHONY: build
build:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: rebuild
rebuild:
	docker-compose down
	docker-compose up -d --build

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: generate
generate:
	alembic revision --autogenerate -m "$(NAME)"