.PHONY: all run test-all benchmark benchmark-keep_all benchmark-non_zero benchmark-non_zero_no_noise benchmark-algo_only help 


all: run

run:
	@echo "Starting FastAPI application..." 
	@uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

test-all:
	@echo "Running All Tests" 
	@pytest ./tests/functional/api/test_url_analysis_endpoint.py::test_url_analysis_valid_empty_data

benchmark: benchmark-algo_only

benchmark-keep_all:
	$(call run_benchmark, 4)
benchmark-non_zero_no_noise:
	$(call run_benchmark, 3)
benchmark-non_zero:
	$(call run_benchmark, 2)
benchmark-algo_only:
	$(call run_benchmark, 1)

define run_benchmark
	@echo "Profiling level set to $(1)"
	$(if $(filter Windows_NT, $(OS)), \
		cmd /C "set ENABLE_PROFILING=$(1) && pytest -m is_profiled ./tests/functional/api/test_url_analysis_endpoint.py", \
		ENABLE_PROFILING=$(1) pytest -m is_profiled ./tests/functional/api/test_url_analysis_endpoint.py)
endef


help:
	@echo "Available targets:"
	@echo "  help                Show this help message"
	@echo "  run           		 Run the API"
	@echo "  test           	 Test the default benchmark (same as benchmark-algo_only)"
	@echo "  benchmark           Run the default benchmark (same as benchmark-algo_only)"
	@echo "  benchmark-algo_only Run the benchmark keeping only algorithm functions"
	@echo "  benchmark-non_zero  Run the benchmark removing uncalled functions"
	@echo "  benchmark-keep_all  Run the benchmark keeping all profiling data"


