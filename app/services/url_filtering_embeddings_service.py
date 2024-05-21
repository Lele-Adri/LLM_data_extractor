import os
from typing import Dict, Set, Tuple

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.app_constants import OPENAI_API_KEY_ENVIRONMENT_VARIABLE_NAME
from app.domain.url_analysis.entities import UrlAnalysisDiscoveredLinks


load_dotenv()

async def filter_relevant_links_using_title(urls_titles: Set[str], target_data_dict: Dict[str, str]) -> UrlAnalysisDiscoveredLinks:
    relevant_links: UrlAnalysisDiscoveredLinks = UrlAnalysisDiscoveredLinks(extracted_links = {key: set() for key in target_data_dict.keys()})
    if len(urls_titles) == 0:
        return relevant_links
    embeddings_model = OpenAIEmbeddings(api_key=os.getenv(OPENAI_API_KEY_ENVIRONMENT_VARIABLE_NAME))
    db = await FAISS.afrom_texts(urls_titles, embeddings_model)
    for data, descr in target_data_dict.items():
        links = db.similarity_search(f"Links that could contain information about [{data}: {descr}]")
        relevant_links.extracted_links[data].update({link.page_content for link in links})
    return relevant_links


async def is_url_relevant_for_data(url: str, data: Tuple[str, str]) -> bool:
    return True
    print("Checking if url is relevant for data....")
    data_name, data_descr = data
    if not url:
        print("Finished checking if url is relevant for data")
        return False
    embeddings_model = OpenAIEmbeddings(api_key=os.getenv(OPENAI_API_KEY_ENVIRONMENT_VARIABLE_NAME))
    try: 
        db = await FAISS.afrom_texts([url], embeddings_model)
    except Exception as e:
        print(e)
    links = db.similarity_search(f"Links that could contain information about [{data_name}: {data_descr}]")
    print("Finished checking if url is relevant for data")
    return len(links) == 0
