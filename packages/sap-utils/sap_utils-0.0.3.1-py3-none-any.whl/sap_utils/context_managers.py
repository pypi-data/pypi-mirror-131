import time


class ExecTimeCM(object):
    """Context manager to be used with the 'with' clause 
    to get the execution time of a code block.
    
    Example Usage:
        with ExecTimeCM() as st:
            print("sample code block.")
    """
    
    def __init__(self, txt="", verbose=True):
        """Called when the context manager scope is initiated.
        """
        self.txt = txt
        self.verbose = verbose
        self.description = f"EXECUTION TIME for {self.txt}"
    
    def __enter__(self):
        """Called when the scope is entered.
        """
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Called when the scope is exited.
        """
        self.exec_time = time.time() - self.start
        if self.verbose:
            print(f"{self.description}: {self.exec_time} seconds")
