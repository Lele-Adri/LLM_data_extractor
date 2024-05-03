from typing import Dict, List, Set

from pydantic import HttpUrl
from helpers.html_content_helpers import normalize_url
from helpers.llm_helpers import get_gpt_4_completion


async def filter_relevant_links_using_title(urls_titles_dict: Dict[str, str], target_data_dict: Dict[str, str]) -> Set[str]:
    # TODO: maybe use some similarity search instead 
    # TODO: and we can return a UrlAnalysisInfoLinks object instead
    subject = ""
    for sub in target_data_dict.values():
        subject += sub + " and "

    titles_list = [urls_titles_dict[title] for title in urls_titles_dict.keys()]

    prompt = f""" You are given a python list with several buttons.
    Each button of the list corresponds to a button coming from a website.
    Do not output your reasoning.
    You are asked to perform the 3 following tasks:
        1. Go through the list of buttons given as input.
        2. Select the buttons that might contain any relevant information about: {subject}\
           Store those buttons in a list. If there are no relevant buttons, create an empty list.
        3. Output the list from step 2.

    Here is the list of buttons: {titles_list}.
    """

    gpt_answer = await get_gpt_4_completion(prompt)

    split_gpt = gpt_answer.split(',')

    good_urls: List[str] = []
    for gpt_title in split_gpt:
        if gpt_title.strip(" ' [ ] ' ") in titles_list:
            stripped_gpt_title = gpt_title.strip(" ' [ ] ' ")
            if not stripped_gpt_title in urls_titles_dict.values():
                good_urls.append(urls_titles_dict[stripped_gpt_title])

    return set([normalize_url(good_url) for good_url in good_urls])
