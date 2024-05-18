
from dataclasses import dataclass
import os
import re
from app.app_constants import ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME

time_threshold = 0.0015
non_algo_paths = {
    "built-in",
    "venv",
    "benchmarks",
    "test",
    "Lib",
    "url_analysis_controller"
}
algo_paths = {
    "LLM_data_extractor"
}


@dataclass
class ProfileOutputDataRow:
    ncalls: str
    tottime: float
    tottime_percall: float
    cumtime: float
    cumtime_percall: float
    filename: str
    lineno: int
    function: str
    builtin: str


def filter_profile_output(profile_output: str) -> str:
    return "\n".join(line for line in profile_output.split("\n") if should_keep_entry(line))


def should_keep_entry(line):
    dataRow: ProfileOutputDataRow = extract_line_data(line)

    enable_profiling_value = float(os.getenv(ENABLE_PROFILING_ENVIRONMENT_VARIABLE_NAME, 0))

    if dataRow is None:
        return True
    path_name = dataRow.filename or dataRow.builtin or ""

    # 1: keep only algo-paths
    if enable_profiling_value == 1:
        if path_includes_excluded_path(path_name) or not path_includes_project_path(path_name):
            return False
    # 2: remove non-zero entries
    if enable_profiling_value == 2:
        if is_row_below_time_threshold(dataRow):
            return False
    # 3: remove non-zero entries & excluded paths
    if enable_profiling_value == 3:
        if path_includes_excluded_path(path_name) or is_row_below_time_threshold(dataRow):
            return False
    return True


def is_row_below_time_threshold(dataRow: ProfileOutputDataRow) -> bool:
    return ((dataRow.tottime < time_threshold and 
             dataRow.tottime_percall < time_threshold) or
            dataRow.ncalls == "0")

def path_includes_project_path(path: str) -> bool: 
    return path_includes_one_of(path, algo_paths)

def path_includes_excluded_path(path: str) -> bool: 
    return path_includes_one_of(path, non_algo_paths)

def path_includes_one_of(path, paths_set) -> bool: 
    return any(_ for _ in paths_set if _ in path)


def extract_line_data(line: str) -> tuple:
    pattern = re.compile(
        r'^\s*(?P<ncalls>\d+/\d+|\d+)\s+'
        r'(?P<tottime>[\d\.]+)\s+'
        r'(?P<percall_tottime>[\d\.]+)\s+'
        r'(?P<cumtime>[\d\.]+)\s+'
        r'(?P<percall_cumtime>[\d\.]+)\s+'
        r'(?:(?P<filename>.+):(?P<lineno>\d+)\((?P<function>.+)\)'
        r'|\{(?P<builtin_method>.+)\})$'
    )

    match = pattern.match(line)
    if match:
        result = match.groupdict()
        return ProfileOutputDataRow(
            ncalls=str(result["ncalls"]),
            tottime=float(result["tottime"]),
            tottime_percall=float(result["percall_tottime"]),
            cumtime=float(result["cumtime"]),
            cumtime_percall=float(result["percall_cumtime"]),
            filename=result.get("filename"),
            lineno=int(result["lineno"]) if result.get("lineno") else None,
            function=result.get("function"),
            builtin=result.get("builtin")
        )
    return None