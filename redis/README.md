# How to run

```
pip install -r requirements.txt
```


### Local

Instalation:
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```

Run:
```
redis-server
```


### Docker

Based on: https://github.com/sameersbn/docker-redis

```
docker stop redis_container
docker rm redis_container
docker build -t redis_image redis/
docker run --name redis_container -d --publish 6379:6379 redis
```


# Test

```
python -m unittest test
```
