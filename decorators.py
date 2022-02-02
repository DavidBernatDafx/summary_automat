
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Running: {func.__name__}")
        func(*args, **kwargs)
        print("Finished: OK\n")
    return wrapper
