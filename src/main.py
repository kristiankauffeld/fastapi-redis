from fastapi import FastAPI
import logging
import redis
from rq import Queue, Worker, Connection
import requests
import time

logging.basicConfig(level=logging.INFO)

app = FastAPI(debug=True)

#redis://default:redis@redis:6379/0

# Establish a connection to Redis
redis_db = redis.Redis(host="redis", port=6379, username="default", password="redis", db=0, decode_responses=True) #db=0

print(f"Ping successful: {redis_db.ping()}")

# Create a queue
task_queue = Queue(connection=redis_db)

# Define the function to be executed by the worker
def count_words_at_url(url):
    """Just an example function that's called async."""
    resp = requests.get(url)
    return len(resp.text.split())

# Enqueue a job
job = task_queue.enqueue(count_words_at_url, 'http://nvie.com')

print('Job id: %s' % job.id)
print('----------------------------------------------------------------------')

# Monitor job status using string values for status
while job.get_status(refresh=True) not in ["finished", "failed"]:
    print('Job %s is currently: %s' % (job.id, job.get_status(refresh=True)))
    time.sleep(5)  # Sleep for a bit before checking the status again to avoid spamming

# Once the loop is exited, check if the job is finished or failed
if job.get_status(refresh=True) == "finished":
    print('Job finished with result:', job.result)
elif job.get_status(refresh=True) == "failed":
    print('Job failed')

# Optionally, print the job result directly (if finished)
# Note: This will be None if the job hasn't finished processing
print('Job result:', job.result)