from fastapi import FastAPI
import logging
import redis
import os
from rq import Queue

logging.basicConfig(level=logging.INFO)

app = FastAPI(debug=True)

#redis://default:redis@redis:6379/0

# Establish a connection to Redis
redis_db = redis.Redis.from_url(os.environ['REDIS_PRIVATE_URL'])
#redis_db = redis.Redis(host="redis", port=6379, username="default", password="redis", db=0)

print(f"Ping successful: {redis_db.ping()}")

# Create a queue
queue = Queue(connection=redis_db)

@app.get("/")
async def root():
    return {"message": "Hello World"}