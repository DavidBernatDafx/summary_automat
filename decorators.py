
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Running: {func.__name__}")
        result = func(*args, **kwargs)
        print("Finished: OK\n")
        return result
    return wrapper
