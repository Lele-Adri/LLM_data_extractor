from typing import Dict
import os


def update_dict_with_new_data(dict_to_update: Dict[str, str], new_data: Dict[str, str]) -> Dict[str, str]:
    for key, new_value in new_data.items():
        if key in dict_to_update:
            if dict_to_update[key] is "":
                dict_to_update[key] = new_value
            else:
                dict_to_update[key] = dict_to_update[key] + "\n" + new_value
    return dict_to_update


def get_test_html_content():
    filename = "./static/atp_rankings.txt"
    full_path = os.path.abspath(filename)
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"


# def load_prompt_template(file_path):
#     with open(file_path, 'r') as file:
#         prompt_text = file.read()
#     return prompt_text
