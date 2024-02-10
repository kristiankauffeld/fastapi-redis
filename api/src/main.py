from fastapi import FastAPI, HTTPException
import logging
import redis
import os
from rq import Queue
from utils.jobs import count_words_at_url

logging.basicConfig(level=logging.INFO)

REDIS_PRIVATE_URL = os.getenv("REDIS_PRIVATE_URL")

app = FastAPI(debug=True)

# Establish a connection to Redis
redis_conn = redis.from_url(REDIS_PRIVATE_URL)
print(f"Ping successful: {redis_conn.ping()}")

# Create a queue
q = Queue(connection=redis_conn)

@app.get("/")
async def root():
    job = q.enqueue(count_words_at_url, 'http://heroku.com')
    return {
        'order_id': job.id,
    }

@app.get("/orders/{order_id}")
def get_order_status(order_id: str):
    job = q.fetch_job(order_id)
    if not job:
        raise HTTPException(status_code=404, detail="Order not found")

    if job.get_status() == 'failed':
        raise HTTPException(status_code=500, detail="Job failed")

    if job.get_status() != 'finished':
        return {
            'status': job.get_status()
        }

    return {
        'status': job.get_status(),
        'result': job.result
    }
    