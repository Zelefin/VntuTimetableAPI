.PHONY: deploy
deploy:
	docker-compose up -d --build

.PHONY: migrate
migrate:
	alembic upgrade head