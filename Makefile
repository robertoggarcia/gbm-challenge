up:
	test -f .env | cp .env.dist .env
	docker-compose -p gbm-challenge up --build --detach

up-windows:
	test -f .env | cp .env.dist .env
	docker-compose -p gbm-challenge up --build --detach app

down:
	docker-compose -p gbm-challenge down

logs:
	docker-compose -p gbm-challenge logs --follow

test:
	docker-compose -p gbm-challenge exec app pytest -v --cov=app tests/

deps:
	poetry install

up-native:
	@
	make deps
	poetry shell
	uvicorn app.main:app --reload
