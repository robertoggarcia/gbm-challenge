up:
	test -f .env | cp .env.dist .env
	docker-compose up --build --detach

down:
	docker-compose down
