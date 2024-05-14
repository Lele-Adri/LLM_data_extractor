import cProfile
import os
import pstats
import io
from functools import wraps

def profiled_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if profiling is enabled via an environment variable
        if os.getenv('ENABLE_PROFILING', False):
            profiler = cProfile.Profile()
            profiler.enable()
            result = func(*args, **kwargs)
            profiler.disable()
            s = io.StringIO()
            ps = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
            ps.print_stats()
            print(s.getvalue())
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper