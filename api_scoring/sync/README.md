# How to run

```
pip install -r requirements.txt
```


### Local

From project folder `scoring-handler`:

```
export FLASK_APP=api_scoring/sync/app/main.py
export FLASK_RUN_PORT=5001
flask run
```


### Docker

Based on: https://github.com/tiangolo/meinheld-gunicorn-flask-docker

```
docker stop scoring_sync_flask_container
docker rm scoring_sync_flask_container
docker build -t scoring_sync_image api_scoring/sync/
docker run --name scoring_sync_flask_container -p 5001:5001 --net host -e BIND="0.0.0.0:5001" scoring_sync_image
```


# Test

```
python -m unittest test
```

# Issues known

* Seems like Flask logs are broken. More info: https://github.com/tiangolo/meinheld-gunicorn-flask-docker/issues/43, https://github.com/mopemope/meinheld/issues/118
