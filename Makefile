up:
	test -f .env | cp .env.dist .env
	docker-compose up --build --detach

down:
	docker-compose down

logs:
	docker-compose logs --follow

test:
	docker-compose exec app pytest -v --cov=app tests/
