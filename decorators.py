
def log_decorator(func):
    """
    Decorator function prints actual running function/method name before
    and finished after decorated function/method was processed

    :param func: decorated function
    :return: wrapper function
    """
    def wrapper(*args, **kwargs):
        print(f"Running: {func.__name__}")
        result = func(*args, **kwargs)
        print("Finished: OK\n")
        return result
    return wrapper
