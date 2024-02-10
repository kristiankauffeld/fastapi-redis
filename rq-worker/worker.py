import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

REDIS_PRIVATE_URL = os.getenv("REDIS_PRIVATE_URL")
redis_conn = redis.from_url(REDIS_PRIVATE_URL)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()