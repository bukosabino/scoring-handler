# How to run

```
pip install -r requirements.txt
```

### Local

From project folder `scoring-handler`:

```
export FLASK_APP=api_model/sync/app/main.py
flask run
```


### Docker

Based on: https://github.com/tiangolo/meinheld-gunicorn-flask-docker

```
docker stop sync_flask_container
docker rm sync_flask_container
docker build -t sync_image api_model/sync/
docker run --name sync_flask_container -p 5000:5000 --net host -e BIND="0.0.0.0:5000" sync_image
```


# Test

```
python -m unittest test
```


# Issues known

* Seems like Flask logs are broken. More info: https://github.com/tiangolo/meinheld-gunicorn-flask-docker/issues/43, https://github.com/mopemope/meinheld/issues/118
