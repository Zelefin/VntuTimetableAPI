.PHONY: deploy
deploy:
	docker-compose up -d --build

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: generate
generate:
	alembic revision --autogenerate -m "$(NAME)"