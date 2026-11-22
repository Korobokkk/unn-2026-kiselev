IMAGE=echo_tg_bot
CONTAINER=curr_echo_tg_bot
ENV=new_bot/.env

.PHONY: build run stop logs format lint run-tests pre-commit

build:
	docker build -t $(IMAGE) .

run: stop
	docker run --detach \
		--name $(CONTAINER) \
		--env-file $(ENV) \
		--restart unless-stopped \
		$(IMAGE)

stop:
	-docker stop $(CONTAINER)
	-docker rm $(CONTAINER)

logs:
	docker logs -f $(CONTAINER)

format:
	black new_bot tests
	ruff format new_bot tests

lint:
	ruff check new_bot tests
	mypy new_bot tests

run-tests:
	PYTHONDONTWRITEBYTECODE=1 pytest tests/

pre-commit: lint run-tests
