.PHONY: deploy
deploy:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: generate
generate:
	alembic revision --autogenerate -m "$(NAME)"