.PHONY: all test-all benchmark run 


all: run

run:
	@echo "Starting FastAPI application..." 
	@uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

test-all:
	@echo "Running All Tests" 
	@pytest ./tests/functional/api/test_url_analysis_endpoint.py::test_url_analysis_valid_empty_data

benchmark:
	@echo "Running benchmarks with profiling" 
ifeq ($(OS), Windows_NT) 
	echo "Running on Windows..."
	cmd /C "set ENABLE_PROFILING=1 && pytest -s ./tests/functional/api/test_url_analysis_endpoint.py::test_url_analysis_valid_empty_data > ./benchmarks/benchmark_results/full_benchmark.txt"
else 
	echo "Running on Unix..."
	ENABLE_PROFILING=1 pytest -s ./tests/functional/api/test_url_analysis_endpoint.py::test_url_analysis_valid_empty_data > ./benchmarks/benchmark_results/full_benchmark.txt
endif
