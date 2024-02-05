from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import aioredis
from aioredis.exceptions import ResponseError

logging.basicConfig(level=logging.INFO)

redis_url="redis://redis:6379"

# Global variable to store the Redis connection
redis_db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_db
    try:
        # using aioredis allow us to interact with Redis without blocking 
        # the server from handling other requests
        redis_db = await aioredis.from_url(redis_url, decode_responses=True)

        if redis_db:
            
            pong = await redis_db.ping()
            print("Redis ping:", pong)
        logging.info(f"Connected to Redis")
    except ResponseError as e:
        logging.error(f"Failed to connect to Redis: {e}")
    yield
    logging.info("Shutting down...")
    await redis_db.close()

app = FastAPI(lifespan=lifespan, debug=True) 



@app.get("/")
async def read_root():
    # Example Redis operation: set a value
    await redis_db.set('my-key', 'value')
    
    # Example Redis operation: get a value
    value = await redis_db.get('my-key', encoding='utf-8')
    return {"Hello": "World", "Redis Value": value}