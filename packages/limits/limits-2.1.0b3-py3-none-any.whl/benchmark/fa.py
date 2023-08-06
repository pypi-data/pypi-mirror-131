import random

from fastapi import FastAPI, HTTPException

from limits.aio import storage
from limits.aio import strategies
from limits import parse


app = FastAPI()

NUM_UNIQUES = 50
LIMIT = parse("100/1 minute")


def random_user():
    return f"192.168.0.{random.randint(0, NUM_UNIQUES)}"


memcached = storage.MemcachedStorage("memcached://localhost:22122", max_connections=50)
redis = storage.RedisStorage("redis://localhost:7379")
mongo = storage.MongoDBStorage("mongodb://localhost:37017")

moving_window_redis = strategies.MovingWindowRateLimiter(redis)
fixed_window_redis = strategies.FixedWindowRateLimiter(redis)
elastic_window_redis = strategies.FixedWindowElasticExpiryRateLimiter(redis)
fixed_window_memcached = strategies.FixedWindowRateLimiter(memcached)
elastic_window_memcached = strategies.FixedWindowElasticExpiryRateLimiter(memcached)
moving_window_mongo = strategies.MovingWindowRateLimiter(mongo)
fixed_window_mongo = strategies.FixedWindowRateLimiter(mongo)
elastic_window_mongo = strategies.FixedWindowElasticExpiryRateLimiter(mongo)


@app.get("/fixed/memcached")
async def fixed_memcached():
    if not await fixed_window_memcached.hit(LIMIT, "fixed-memcached", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"

@app.get("/elastic/memcached")
async def elastic_memcached():
    if not await elastic_window_memcached.hit(
        LIMIT, "elastic-memcached", random_user()
    ):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"

@app.get("/fixed/redis")
async def fixed_redis():
    if not await fixed_window_redis.hit(LIMIT, "fixed-redis", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"


@app.get("/elastic/redis")
async def elastic_redis():
    if not await elastic_window_redis.hit(LIMIT, "elastic-redis", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"


@app.get("/moving/redis")
async def moving_redis():
    if not await moving_window_redis.hit(LIMIT, "moving-redis", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"

@app.get("/fixed/mongo")
async def fixed_mongo():
    if not await fixed_window_mongo.hit(LIMIT, "fixed-mongo", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"


@app.get("/elastic/mongo")
async def elastic_mongo():
    if not await elastic_window_mongo.hit(LIMIT, "elastic-mongo", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"


@app.get("/moving/mongo")
async def moving_mongo():
    if not await moving_window_mongo.hit(LIMIT, "moving-mongo", random_user()):
        raise HTTPException(status_code=429, detail="Too much")

    return "42"
