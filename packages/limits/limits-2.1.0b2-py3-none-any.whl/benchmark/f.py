import random

from flask import Flask, abort

from limits import storage
from limits import strategies
from limits import parse


app = Flask(__name__)

NUM_UNIQUES = 50
LIMIT = parse("100/10 seconds")


def random_user():
    return f"192.168.0.{random.randint(0, NUM_UNIQUES)}"


memcached = storage.MemcachedStorage("memcached://localhost:22122", max_pool_size=50)
redis = storage.RedisStorage("redis://localhost:7379")
mongo = storage.MongoDBStorage("mongodb://localhost:37017")

moving_window_redis = strategies.MovingWindowRateLimiter(redis)
fixed_window_redis = strategies.FixedWindowRateLimiter(redis)
fixed_window_memcached = strategies.FixedWindowRateLimiter(memcached)
elastic_window_redis = strategies.FixedWindowElasticExpiryRateLimiter(redis)
elastic_window_memcached = strategies.FixedWindowElasticExpiryRateLimiter(memcached)
moving_window_mongo = strategies.MovingWindowRateLimiter(mongo)
fixed_window_mongo = strategies.FixedWindowRateLimiter(mongo)
elastic_window_mongo = strategies.FixedWindowElasticExpiryRateLimiter(mongo)


@app.get("/fixed/memcached")
def fixed_memcached():
    if not fixed_window_memcached.hit(LIMIT, "fixed-memcached", random_user()):
        abort(429)

    return "42"


@app.get("/fixed/redis")
def fixed_redis():
    if not fixed_window_redis.hit(LIMIT, "fixed-redis", random_user()):
        abort(429)

    return "42"


@app.get("/elastic/redis")
def elastic_redis():
    if not elastic_window_redis.hit(LIMIT, "elastic-redis", random_user()):
        abort(429)

    return "42"


@app.get("/elastic/memcached")
def elastic_memcached():
    if not elastic_window_memcached.hit(LIMIT, "elastic-memcached", random_user()):
        abort(429)

    return "42"


@app.get("/moving/redis")
def moving_redis():
    if not moving_window_redis.hit(LIMIT, "moving-redis", random_user()):
        abort(429)

    return "42"

@app.get("/fixed/mongo")
def fixed_mongo():
    if not fixed_window_mongo.hit(LIMIT, "fixed-mongo", random_user()):
        abort(429)

    return "42"


@app.get("/elastic/mongo")
def elastic_mongo():
    if not elastic_window_mongo.hit(LIMIT, "elastic-mongo", random_user()):
        abort(429)

    return "42"

@app.get("/moving/mongo")
def moving_mongo():
    if not moving_window_mongo.hit(LIMIT, "moving-mongo", random_user()):
        abort(429)

    return "42"
