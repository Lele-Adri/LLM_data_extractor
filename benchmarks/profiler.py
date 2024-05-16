from threading import Lock
import cProfile
import os
import pstats
import io
from functools import wraps

profiler_lock = Lock()

def profiled_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if profiling is enabled via an environment variable
        if os.getenv('ENABLE_PROFILING', False):
            with profiler_lock:
                profiler = cProfile.Profile()
                try: 
                    profiler.enable()
                    result = func(*args, **kwargs)
                finally: 
                    profiler.disable()
                    s = io.StringIO()
                    ps = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
                    ps.print_stats()
                    # TODO: write to file 
                    print(s.getvalue())
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper