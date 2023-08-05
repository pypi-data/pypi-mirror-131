import time
import functools

from typing import Callable

    
def timeit(function):
    """Decorator to check the execution time for a function.

    Args:
        function (Callable): Function for which the time is to be checked.

    Returns:
        Callable: Returns the wrapped function that can print the execution time.
    
    Example:
        @timeit
        def random_function():
            <code>
    """
    
    @functools.wraps(function)    # ensures that the function meta data stays the same and is not overwritten by the decorator.
    def time_wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        print(f"\nTIMEIT: Time to execute function {function.__name__}: {time.time() - start_time} seconds.\n")
        
        return result
    return time_wrapper