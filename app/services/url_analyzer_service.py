from typing import Any, Dict, Set
from pydantic import HttpUrl
from models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel

async def test_analyze_url(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    extracted_data = {"url": params.url, "parameters": params.parameters, "test": "test"}
    return UrlAnalysisResponseModel(extracted_data=extracted_data)

async def analyse_url(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    extracted_data = {key: None for key in params.parameters}
    links_to_visit = {params.url}
    visited_links = set()
    while len(links_to_visit) > 0:
        current_link = links_to_visit.pop()
        if current_link in visited_links: 
            continue
        visited_links.add(current_link)
        html_content = download_link_content(current_link)
        extracted_data = update_extracted_data(html_content)
        extracted_links_from_anchor_tags = extract_links_from_anchor_tags(html_content)
        new_links = extracted_links_from_anchor_tags - visited_links - links_to_visit
        potentially_relevant_links = await filter_relevant_links_using_title(new_links, params.parameters)
        links_to_visit.update(potentially_relevant_links)
    
    return UrlAnalysisResponseModel(extracted_data=extracted_data)

# TODO: Implement and adapt "Any"s
def download_link_content(url: HttpUrl) -> Any:
    return

def extract_links_from_anchor_tags(html_content: Any) -> Set[HttpUrl]:
    return

async def filter_relevant_links_using_title(links_set: Set[HttpUrl], target_data_dict: Dict[str, str]) -> Set[HttpUrl]:
    return

async def update_extracted_data(html_content: Any) -> Dict[str, Any]:
    return