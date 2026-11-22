IMAGE=echo_tg_bot
CONTAINER=curr_echo_tg_bot
ENV=new_bot/.env

.PHONY: install build run stop logs ruff-cs-check ruff-linter-check mypy-check run-tests pre-commit

install:
	uv sync --dev

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


ruff-cs-check:
	uv run ruff format --check new_bot tests/

ruff-linter-check:
	uv run ruff check new_bot tests/

mypy-check:
	uv run mypy

run-tests:
	PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/

pre-commit: ruff-cs-check ruff-linter-check mypy-check run-tests
