import cProfile
from datetime import datetime
import io
import os
import pstats
import warnings

import pytest
from app.app_constants import BENCHMARK_RESULTS_DIRECTORY_NAME, ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME, IS_PROFILED_ATTRIBUTE_NAME
from app.helpers.helpers import try_save_benchmark_results_to_file
from benchmarks.cProfile_output_helper import filter_profile_output



def pytest_collection_modifyitems(config, items):
    """
    Pytest hook to add profiler marker.
    This allows to only run benchmarked tests, using the command:
        pytest -m is_profiled
    """
    for item in items:
        if IS_PROFILED_ATTRIBUTE_NAME in getattr(item, 'fixturenames', ()):
            item.add_marker(IS_PROFILED_ATTRIBUTE_NAME)


@pytest.fixture
def is_profiled(request):
    if float(os.getenv(ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME, 0)):
        profiler = cProfile.Profile()
        profiler.enable()

        yield profiler

        profiler.disable()
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
        ps.print_stats()
        profile_output = s.getvalue()
        profile_output = filter_profile_output(profile_output)
        current_function_name = request.node.name
        benchmark_filename = f"{current_function_name}_{datetime.now().strftime('%d-%m_%H-%M-%S')}_profile.txt"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_relative_file_path = f"../benchmarks/{BENCHMARK_RESULTS_DIRECTORY_NAME}/{benchmark_filename}"
        output_file_path = os.path.join(script_dir, output_relative_file_path)
        results_saved = try_save_benchmark_results_to_file(output_file_path, profile_output)
        if not results_saved:
            warnings.warn("Unexpected error writing results to file.")

