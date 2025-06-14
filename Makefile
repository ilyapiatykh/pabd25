IMAGE_NAME = pabd25
CONTAINER_NAME = $(IMAGE_NAME)
ENV_FILE = .env

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d \
		-p 8000:8000 \
		--env-file $(ENV_FILE) \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME)


clean:
	docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	docker rmi -f $(IMAGE_NAME) 2>/dev/null || true

up: build run

help:
	@echo "Использование:"
	@echo "  make build   - Собрать Docker-образ"
	@echo "  make run     - Запустить контейнер"
	@echo "  make up      - Собрать образ и запустить контейнер"
	@echo "  make clean   - Очистить контейнеры и образы"
	@echo "  make help    - Показать это сообщение"
