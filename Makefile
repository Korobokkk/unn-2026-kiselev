IMAGE=echo_tg_bot
CONTAINER=curr_echo_tg_bot
ENV=python_first_v_bot/.env

.PHONY: build run stop logs

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
