# pylint: disable=import-error, line-too-long
"""Redis Helpers"""
import os
from dotenv import load_dotenv
from redis import Redis
from rq_scheduler import Scheduler
import cbor2
import pendulum

load_dotenv()

REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_USERNAME = os.getenv('REDIS_USERNAME')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


def initialize_redis():
    """
    Inits Redis producer
    """
    return Redis(host=REDIS_SERVER, port=REDIS_PORT, db=0, username=REDIS_USERNAME, password=REDIS_PASSWORD)


def schedule_task(execute_at, task_function, task_args):
    """Schedules a task
        Args:
        execute_at - Task execution date time in UTC
        task_function - function to execute
        args - function arguments
    """
    redis_client = initialize_redis()
    scheduler = Scheduler('retail', connection=redis_client)
    scheduler.enqueue_at(execute_at, task_function, task_args)


def schedule_periodic_job(first_execution_time, task_function, task_args, **kwargs) -> None:
    """Schedules a task
        Args:
        first_execution_time:  Time for first execution, in UTC timezone
        task_function: Function to be queued
        task_args: Arguments passed into function when executed
        :key interval: Time before the function is called again, in seconds
        :key repeat: Repeat this number of times (None means repeat forever)
        :key meta: Arbitrary pickleable data on the job itself
        :key kwargs: Keyword arguments passed into function when executed
    """
    interval = kwargs['interval']
    repeat = kwargs['repeat']
    meta = kwargs['meta']
    redis_client = initialize_redis()
    scheduler = Scheduler('retail', connection=redis_client)
    scheduler.schedule(
        scheduled_time=first_execution_time,
        func=task_function,
        args=task_args,
        interval=interval,
        repeat=repeat,
        meta=meta
    )


def set_key(key: str, val):
    """ Sets key value pair in redis
    Args:
    key: Key name
    val: Data to be stored in key
    expire_in: TTL of the key in seconds
    keepttl: Whether to or not to keep existing TTL
    """
    redis_client = initialize_redis()
    redis_client.set(key, val)


def set_expiring_key(key: str, val, expire_in: int, keepttl: bool = True):
    """ Sets data in an expiring key
    Args:
    key: Key name
    val: Data to be stored in key
    expire_in: TTL of the key in seconds
    keepttl: Whether to or not to keep existing TTL
    """
    redis_client = initialize_redis()
    # First check TTL
    ttl = redis_client.ttl(key)
    redis_client.set(key, val, keepttl=keepttl)

    if ttl < 0:
        redis_client.expire(key, expire_in)


def search_keys(pattern: str):
    """Search redis for keys
    Args:
    ``pattern``: Pattern to match
    """
    redis_client = initialize_redis()
    data = {}
    cursor = '0'
    while cursor != 0:
        cursor, keys = redis_client.scan(
            cursor=cursor, match=pattern, count=100000)
        if keys:
            values = redis_client.mget(*keys)
            values = [value for value in values if not value is None]
            keys = [key.decode("utf-8") for key in keys]
            data.update(dict(zip(keys, values)))
    return data


def get_value(key: str):
    """ Get value of a key
    Args:
    key: Key name
    """
    redis_client = initialize_redis()
    return redis_client.get(name=key)

# keyz = search_keys('*ACTIVE_CUSTOMER:20200828*')
# print(keyz)
# for key in keyz:
    # print(cbor2.loads(keyz[key]))

    
def search_results(primary_key: str, sales_rep: str, start_date: str, end_date: str):
    """Searches Redis for range of dates
        Args:
        primary_key: Whether ACTIVE_CUSTOMER or ACCOUNT_DUE
        start_date: Start date of range
        end_date: End date of range
    """
    start = pendulum.parse(start_date).set(
        tz="Africa/Nairobi").start_of('day')
    stop = pendulum.parse(end_date).set(
        tz="Africa/Nairobi").end_of('day')
    result = []
    for day in range(start.diff(stop).in_days()+1):
        date_string = start.add(days=day).format('YYYYMMDD')
        result.append(search_keys(f'{primary_key}:{date_string}:{sales_rep}*'))
    result_dict = {}
    for item in result:
        result_dict.update(dict(zip(item.keys(), item.values())))
    return result_dict


