import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️ {func.__name__} ran in {end - start:.2f} seconds.")
        return result
    return wrapper

def print_success(message):
    print(f"\033[92m✔ {message}\033[0m")

def print_error(message):
    print(f"\033[91m✖ {message}\033[0m")
