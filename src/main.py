from fastapi import FastAPI
import logging
import redis
import os
from rq import Queue

logging.basicConfig(level=logging.INFO)

REDISHOST = os.getenv("REDISHOST")
REDISPORT = os.getenv("REDISPORT")
REDISUSER = os.getenv("REDISUSER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

REDIS_PRIVATE_URL = os.getenv("REDIS_PRIVATE_URL")

app = FastAPI(debug=True)

# Establish a connection to Redis
redis_db = redis.from_url(REDIS_PRIVATE_URL + "?decode_responses=True&health_check_interval=2")

#redis_db = redis.Redis(host=REDISHOST, port=REDISPORT, username=REDISUSER, password=REDIS_PASSWORD, db=0)

print(f"Ping successful: {redis_db.ping()}")

# Create a queue
queue = Queue(connection=redis_db)

@app.get("/")
async def root():
    return {"message": "Hello World"}