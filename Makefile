PROJECT_NAME=chat_websockets

all: run

run:
	@docker-compose up chat_websockets_app

stop:
	@docker-compose stop

clean:
	@docker-compose down

bash:
	@docker exec -it chat_websockets bash

lint:
	@docker-compose run --rm $(PROJECT_NAME)_app flake8 $(PROJECT_NAME)

test: lint
	@docker-compose up test
	@docker-compose stop test

adev:
	adev runserver ./chat_websockets/__main__.py -p 8080
