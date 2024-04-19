test = [1, 2, 3]
dict = {"a": 1, "b": 2, "c": 3}
sought_data_str = '\n'.join(f"\t\t'{key}': {value}" for key, value in dict.items())
print(sought_data_str)