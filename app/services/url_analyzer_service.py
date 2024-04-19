from typing import Any, Dict, Set, Tuple, List
from pydantic import HttpUrl
from models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel, \
     UrlAnalysisInfoLinks
from bs4 import BeautifulSoup
import requests
from openai import OpenAI
from helpers.helpers import get_test_html_content, update_dict_with_new_data
from services.data_extraction import extract_information_from_url


async def test_scrape_and_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    extracted_data = {"url": params.url, "parameters": params.sought_data, "test": "test"}
    return UrlAnalysisResponseModel(extracted_data=extracted_data)

async def scrape_and_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    extracted_data = {key: "" for key in params.sought_data}
    links_to_visit = {params.url}
    visited_links = set()
    while len(links_to_visit) > 0:
        current_link = links_to_visit.pop()
        if current_link in visited_links:
            continue
        visited_links.add(current_link)
        html_content, extracted_dict_from_anchor_tags, extracted_title_from_anchor_tags, extracted_link_from_anchor_tags = download_link_content(current_link)
        extracted_data = update_extracted_data(html_content)
        #extracted_links_from_anchor_tags = extract_links_from_anchor_tags(soup_object)
        #new_links = extracted_link_from_anchor_tags - visited_links - links_to_visit
        #potentially_relevant_links = await filter_relevant_links_using_title(new_links, params.parameters)
        #links_to_visit.update(potentially_relevant_links)

    return UrlAnalysisResponseModel(extracted_data=extracted_data)

# TODO: Implement and adapt "Any"s
async def download_link_content(params: UrlAnalysisRequestParams) -> UrlAnalysisInfoLinks:

    # extract links using BeautifulSoup
    r = requests.get(params.url)
    soup = BeautifulSoup(r.content, 'html.parser')

    links = soup.find_all("a") # Find all elements with the tag <a>

    title_link_dict = {}
    for link in links:
        href_link = str(link.get("href"))

        if href_link.startswith("http"):
            total_link = href_link
        else:
            total_link = str(params.url) + href_link

        title_link_dict[str(link.string).strip(" \n ")] = total_link

    # remove duplicate urls from dict
    cleaned_dict = {}
    for key,value in title_link_dict.items():
        if value not in cleaned_dict.values():
            cleaned_dict[key] = value

    # create list with titles and list with links frolm the dictionary
    title_list = []
    link_list = []
    for key, value in cleaned_dict.items():
        title_list.append(key)
        link_list.append(value)

    return UrlAnalysisInfoLinks(html_content=r.text,
                                link_dictionary=cleaned_dict,
                                titles_set=set(title_list),
                                urls_set=set(link_list))

#def extract_links_from_anchor_tags(soup: Any) -> Set[HttpUrl]:
#    soup.findAll('a', href=True, text='TEXT')
#    return

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
    llm_model = "gpt-4-1106-preview"

    # get the answer of gpt (str)
    gpt_answer = await get_completion(prompt, model=llm_model)

    # create a list containing all the titles
    split_gpt = gpt_answer.split(',')

    # get the urls linked to those titles
    good_urls = []
    good_titles = []
    for gpt_title in split_gpt:
        stripped_gpt_title = gpt_title.strip(" ' [ ] ")
        good_titles.append(stripped_gpt_title)
        good_urls.append(HttpUrl(titles_urls_dict[stripped_gpt_title]))
    return set(good_titles), set(good_urls)

async def get_completion(prompt, model):
    messages = [{"role": "user", "content": prompt}]
    client = OpenAI(api_key='######')
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

async def update_extracted_data(html_content: Any) -> Dict[str, Any]:
    return

async def download_link_content_test(url: HttpUrl, use_test_file=False) -> str:
    if use_test_file:
        return get_test_html_content()
    try: 
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                  }
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url) # TODO: make async
        return response.text  
    except requests.RequestException as e:
        return str(e)  

