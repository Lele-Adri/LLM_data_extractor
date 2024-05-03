import os
from typing import Dict, List, Set, Tuple

from dotenv import load_dotenv
from pydantic import HttpUrl
from helpers.html_content_helpers import normalize_url
from helpers.llm_helpers import get_gpt_4_completion
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

async def filter_relevant_links_using_title(urls_titles: Set[str], target_data_dict: Dict[str, str]) -> Set[str]:
    if len(urls_titles) == 0: 
        return set()
    embeddings_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.from_texts(urls_titles, embeddings_model)
    relevant_links: Set[str] = set()
    for data, descr in target_data_dict.items():
        links = db.similarity_search(f"Links that could contain information about [{data}: {descr}]")
        relevant_links = relevant_links.union({link.page_content for link in links})
    return relevant_links