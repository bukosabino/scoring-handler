# How to run

```
pip install -r requirements.txt
```

### Local

From project folder `scoring-handler`:

```
uvicorn api_model.asynch.app.main:app
```


### Docker

Based on: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

```
docker stop async_fastapi_container
docker rm async_fastapi_container
docker build -t async_image api_model/asynch/
docker run --name async_fastapi_container -p 8000:8000 --net host -e BIND="0.0.0.0:8000" async_image
```

# Test

```
python -m unittest test
```
