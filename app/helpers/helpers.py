
def try_save_benchmark_results_to_file(output_file_path: str, content: str) -> bool:
    try: 
        with open(output_file_path, 'w') as f:
            f.write(content)
    except Exception as e:
        return False
    return True