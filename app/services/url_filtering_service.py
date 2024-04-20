from typing import Dict, Set, Tuple

from pydantic import HttpUrl
from helpers.llm_helpers import get_gpt_4_completion


async def filter_relevant_links_using_title(titles_urls_dict: Dict, titles_list: Set[str], target_data_dict: Dict[str, str]) -> Tuple[Set[str], Set[HttpUrl]]:
    # input: * set with urls of links
    #        * params.parameters: dict containing keys and values describing infos
    #          we are looking for
    #
    # output: * set with urls of links

    subject = "the investment strategy of the firm."
    titles = titles_list

    prompt = f""" You are given a python list with several elements.
    Each element of the list is a button coming from a website.
    Do not output your reasoning.
    You are asked to perform the following tasks:
        1. Go through the list of buttons given as input.
        2. Select the buttons that might contain any relavant information about {subject} and store them in a list.
        3. Output the list from step 2.

    Here is the list of titles: {titles}.
    """

    gpt_answer = await get_gpt_4_completion(prompt)

    split_gpt = gpt_answer.split(',')

    good_urls = []
    good_titles = []
    for gpt_title in split_gpt:
        stripped_gpt_title = gpt_title.strip(" ' [ ] ")
        good_titles.append(stripped_gpt_title)
        good_urls.append(HttpUrl(titles_urls_dict[stripped_gpt_title]))
    return set(good_titles), set(good_urls)
