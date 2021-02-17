init:
	pip install -r requirements.txt

isort:
	isort --check-only --recursive api_model api_scoring redis benchmark

format: isort
	black api_model api_scoring redis benchmark

isort-fix:
	isort --recursive api_model api_scoring redis benchmark

lint: isort
	prospector api_model/
	prospector api_scoring/
	prospector redis/
	prospector benchmark/

test: lint
	coverage run -m unittest test
	coverage report -m

docker-stop:
	docker stop async_fastapi_container
	docker rm async_fastapi_container

	docker stop sync_flask_container
	docker rm sync_flask_container

	docker stop scoring_async_fastapi_container
	docker rm scoring_async_fastapi_container

	docker stop scoring_sync_flask_container
	docker rm scoring_sync_flask_container

	docker stop redis_container
	docker rm redis_container

docker-build:
	docker build -t async_image api_model/asynch/
	docker build -t sync_image api_model/sync/
	docker build -t scoring_async_image api_scoring/asynch/
	docker build -t scoring_sync_image api_scoring/sync/
	docker build -t redis_image redis/

docker-run-model-async:
	docker run --name async_fastapi_container -p 8000:8000 --net host -e BIND="0.0.0.0:8000" async_image

docker-run-model-sync:
	docker run --name sync_flask_container -p 5000:5000 --net host -e BIND="0.0.0.0:5000" sync_image

docker-run-scoring-async:
	docker run --name scoring_async_fastapi_container -p 8001:8001 --net host -e BIND="0.0.0.0:8001" scoring_async_image

docker-run-scoring-sync:
	docker run --name scoring_sync_flask_container -p 5001:5001 --net host -e BIND="0.0.0.0:5001" scoring_sync_image

docker-run-redis:
	docker run --name redis_container -d --publish 6379:6379 redis
