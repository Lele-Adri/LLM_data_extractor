import os
from typing import Dict, List, Set, Tuple

from dotenv import load_dotenv
from pydantic import HttpUrl
from app.helpers.html_content_helpers import normalize_url
from app.helpers.llm_helpers import get_gpt_4_completion
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.models.url_analysis import UrlAnalysisDiscoveredLinks


load_dotenv()

async def filter_relevant_links_using_title(urls_titles: Set[str], target_data_dict: Dict[str, str]) -> UrlAnalysisDiscoveredLinks:
    relevant_links: UrlAnalysisDiscoveredLinks = UrlAnalysisDiscoveredLinks(extracted_links = {key: set() for key in target_data_dict.keys()})
    if len(urls_titles) == 0:
        return relevant_links
    embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.from_texts(urls_titles, embeddings_model)
    for data, descr in target_data_dict.items():
        links = db.similarity_search(f"Links that could contain information about [{data}: {descr}]")
        relevant_links.extracted_links[data].update({link.page_content for link in links})
    return relevant_links
