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


def print_debugging_markers(function):
    """Decorator to print at the entry and exit of a function.

    Args:
        function (Callable): Function for which debugging markers are to be printed.

    Returns:
        Callable: Returns the wrapped function that can print the debugging markers.
    
    Example:
        @print_debugging_markers
        def random_function():
            <code>
    """
    
    @functools.wraps(function)    # ensures that the function meta data stays the same and is not overwritten by the decorator.
    def dpm_wrapper(*args, **kwargs):
        print(f">>>>> ENTERING the function {function.__name__}({args}, {kwargs})")    # TODO: Print the argument better.
        result = function(*args, **kwargs)
        print(f"<<<<< EXITING the function {function.__name__}(...)")
        
        return result

    return dpm_wrapper