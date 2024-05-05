from typing import Dict, List, Set

from pydantic import HttpUrl
from app.helpers.url_analysis_helpers import normalize_url
from app.helpers.llm_helpers import get_gpt_4_completion

import weaviate, os
from weaviate import EmbeddedOptions
import openai

from dotenv import load_dotenv, find_dotenv


# UNUSED -- KEPT FOR REFERENCE

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


async def filter_relevant_links_using_title_2(urls_titles_dict: Dict[str, str], target_data_dict: Dict[str, str]) -> Set[str]:
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

    return set(good_urls)


async def filter_relevant_links_using_embeddings(titles_urls_dict: Dict, titles_list: Set[str], target_url: HttpUrl ,target_data_dict: Dict[str, str], dist_treshold: float) -> Set[HttpUrl]:
    # input: * set with urls of links
    #        * params.parameters: dict containing keys and values describing infos
    #          we are looking for
    #
    # output: * set with urls of links

    concept_data = list(target_data_dict.keys())
    list_values = list(target_data_dict.values())
    concept_data.extend(list_values)

    # remove pairs with None as title

    if bool(titles_urls_dict):
        formated_data = []
        for title, url in titles_urls_dict.items():
            if title != "None":
                formated_data.append({
                    'Title': title,
                    'URL': url
                })

        # use Weaviate to create embeddings and filter titles

        ## create a client
        client = await create_client()

        ## create class object
        await create_embed_object(client)

        ## add data to the object
        await add_data(client, formated_data)

        ## get output from filtering
        first_filter_urls = await get_good_urls(client, concept_data, dist_treshold)

        ## remove links coming from another website
        good_urls = await remove_external_urls(first_filter_urls, target_url)


    return set(good_urls)


async def create_client():

    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']

    client = weaviate.Client(
        embedded_options=EmbeddedOptions(),
        additional_headers={
            #"X-OpenAI-BaseURL": os.environ['OPENAI_API_BASE'],
            "X-OpenAI-Api-Key": openai.api_key  # Replace this with your actual key
        }
    )

    return client

async def create_embed_object(client):
    if client.schema.exists("Title"):
        client.schema.delete_class("Title")
    class_obj = {
        "class": "Title",
        "vectorizer": "text2vec-openai",  # Use OpenAI as the vectorizer
        "moduleConfig": {
            "text2vec-openai": {
                "model": "ada",
                "modelVersion": "002",
                "type": "text",
            # "baseURL": os.environ["OPENAI_API_BASE"]
            }
        }
    }

    client.schema.create_class(class_obj)

    #return client

async def add_data(client, data):

    with client.batch.configure(batch_size=5) as batch:
        for i, d in enumerate(data):  # Batch import data

            properties = {
                "title": d["Title"],
                "url": d["URL"],
            }

            batch.add_data_object(
                data_object=properties,
                class_name="Title"
            )

    #return client

async def get_good_urls(client, concepts, dist_treshold):

    response = (
    client.query
    .get("Title", ["title", "url"])
    .with_near_text({"concepts": concepts, "distance": dist_treshold})
    .do()
    )

    print("heloooooo \n")
    print(response)

    list_with_dicts = response["data"]["Get"]["Title"]

    # create a list with urls only
    list_with_urls = []
    for dictionary in list_with_dicts:
        list_with_urls.append(dictionary.get("url"))

    return list_with_urls

async def remove_external_urls(urls, main_url):

    start_of_url = await get_start_url(str(main_url))

    output_url = []
    for url in urls:

        if str(url).startswith(start_of_url):

            output_url.append(url)

    return output_url

async def get_start_url(url):

    rebuild_url = ""
    for items in url.split(".")[:-1]:

        rebuild_url += items + "."

    return rebuild_url[:-1]
