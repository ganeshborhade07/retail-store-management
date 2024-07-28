import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def measure_latency(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        latency = end_time - start_time
        print(f"Function '{func.__name__}' executed in {latency:.4f} seconds")
        return result
    return wrapper
