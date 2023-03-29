up:
	test -f .env | cp .env.dist .env
	docker-compose -p gbm-challenge up --build --detach

down:
	docker-compose -p gbm-challenge down

logs:
	docker-compose -p gbm-challenge logs --follow

test:
	docker-compose exec app pytest -v --cov=app tests/
