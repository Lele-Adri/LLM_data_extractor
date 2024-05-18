from app.app_constants import IS_PROFILED_ATTRIBUTE_NAME



def pytest_collection_modifyitems(config, items):
    """
    Pytest hook to add profiler marker.
    This allows to only run benchmarked tests, using the command:
        pytest -m is_profiled
    """
    for item in items:
        if hasattr(item.function, IS_PROFILED_ATTRIBUTE_NAME):
            item.add_marker(IS_PROFILED_ATTRIBUTE_NAME)