# How to run

```
pip install -r requirements.txt
```


### Local

From project folder `scoring-handler`:

```
uvicorn api_scoring.asynch.app.main:app --port 8001
```


### Docker

Based on: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

```
docker stop scoring_async_fastapi_container
docker rm scoring_async_fastapi_container
docker build -t scoring_async_image api_scoring/asynch/
docker run --name scoring_async_fastapi_container -p 8001:8001 --net host -e BIND="0.0.0.0:8001" scoring_async_image
```


# Test

```
python -m unittest test
```
