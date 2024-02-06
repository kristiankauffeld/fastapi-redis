from fastapi import FastAPI
import logging
import redis
from rq import Queue
import requests
import time
from rq.job import Job

logging.basicConfig(level=logging.INFO)

app = FastAPI(debug=True)

# Establish a connection to Redis
r = redis.Redis(host="redis", port=6379, username="default", password="redis", decode_responses=True) #db=0

print(f"Ping successful: {r.ping()}")

# Create a queue
task_queue = Queue(connection=r)

def count_words_at_url(url):
    """Just an example function that's called async."""
    resp = requests.get(url)
    return len(resp.text.split())

# Enqueue a job
job = task_queue.enqueue(count_words_at_url, 'http://nvie.com')
#task_queue.enqueue(count_words_at_url, 'http://nvie.com')

print('Job id: %s' % job.id)
print('Status: %s' % job.get_status(refresh=True))
print(job.return_value)
#result = Job.fetch(id=job.id, connection=r)

#result.latest_result()  #  returns Result(id=uid, type=SUCCESSFUL)

#if result == result.Type.SUCCESSFUL: 
#    print(result.return_value) 
#else: 
#    print(result.exc_string)


#print(job.return_value)
#result = job.latest_result() 

#print(result.created_at)
#print(result.type)

#job = Job.fetch(id='my_id', connection=redis)
#for result in job.results(): 
#    print(result.created_at, result.type)

#if result == result.Type.SUCCESSFUL: 
#    print(result.return_value) 
#else: 
#    print(result.exc_string)

#if status == "finished":
#    print(job.return_value)

#redis_url = 'redis://redis:6379'

#redis://[[username]:[password]]@localhost:6379/0
#r = redis.from_url(url="redis://default:admin@redis:6379/0")