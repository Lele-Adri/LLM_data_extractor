from typing import Dict




def update_dict_with_new_data(dict_to_update: Dict[str, str], new_data: Dict[str, str]) -> Dict[str, str]:
    for key, new_value in new_data.items():
        if key in dict_to_update:
            if dict_to_update[key] == "":
                dict_to_update[key] = new_value
            else:
                dict_to_update[key] = dict_to_update[key] + "\n" + new_value
    return dict_to_update


