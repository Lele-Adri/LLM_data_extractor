import asyncio
import io
from threading import Lock
import os
import cProfile, pstats
from functools import wraps
from datetime import datetime
import warnings
from app.app_constants import *
from app.helpers.helpers import try_save_benchmark_results_to_file
from dataclasses import dataclass

from benchmarks.cProfile_output_helper import filter_profile_output


enable_profiling_value = float(os.getenv(ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME, 0))
profiler_lock = Lock()

def profiled_function(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if enable_profiling_value:
            with profiler_lock:
                profiler = cProfile.Profile()
                try: 
                    profiler.enable()
                    result = await await_if_coroutine(func, *args, **kwargs)
                finally: 
                    profiler.disable()
                    s = io.StringIO()
                    ps = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
                    ps.print_stats()
                    profile_output = s.getvalue()
                    profile_output = filter_profile_output(profile_output)
                    benchmark_filename = f"{func.__name__}_{datetime.now().strftime("%d-%m_%H-%M-%S")}_{enable_profiling_value}.txt"
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    output_relative_file_path = f"{BENCHMARK_RESULTS_DIRECTORY_NAME}/{benchmark_filename}"
                    output_file_path = os.path.join(script_dir, output_relative_file_path)
                    results_saved = try_save_benchmark_results_to_file(output_file_path, profile_output)
                    if not results_saved:
                        warnings.warn("Unexpected error writing results to file.")
                    return result
        else:
            result = await await_if_coroutine(func, *args, **kwargs)
        return result

    setattr(wrapper, IS_PROFILED_ATTRIBUTE_NAME, True)
    return wrapper


async def await_if_coroutine(func, *args, **kwargs):
    return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
