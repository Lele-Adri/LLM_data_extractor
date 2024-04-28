from typing import Dict, Set, Tuple

from pydantic import HttpUrl
from app.helpers.llm_helpers import get_gpt_4_completion


async def filter_relevant_links_using_title(titles_urls_dict: Dict, titles_list: Set[str], target_data_dict: Dict[str, str]) -> Set[HttpUrl]:
    # input: * set with urls of links
    #        * params.parameters: dict containing keys and values describing infos
    #          we are looking for
    #
    # output: * set with urls of links

    subject = ""
    for sub in target_data_dict.values():
        subject += sub + " and "

    titles = titles_list

    prompt = f""" You are given a python list with several buttons.
    Each button of the list corresponds to a button coming from a website.
    Do not output your reasoning.
    You are asked to perform the 3 following tasks:
        1. Go through the list of buttons given as input.
        2. Select the buttons that might contain any relavant information about: {subject}\
           Store those buttons in a list. If there are no relevant buttons, create an empty list.
        3. Output the list from step 2.

    Here is the list of buttons: {titles}.
    """

    gpt_answer = await get_gpt_4_completion(prompt)

    split_gpt = gpt_answer.split(',')

    good_urls = []
    for gpt_title in split_gpt:

        if gpt_title.strip(" ' [ ] ' ") in titles_list:

            stripped_gpt_title = gpt_title.strip(" ' [ ] ' ")
            if not titles_urls_dict[stripped_gpt_title].endswith("None"):

                good_urls.append(HttpUrl(titles_urls_dict[stripped_gpt_title]))

    return set(good_urls)
