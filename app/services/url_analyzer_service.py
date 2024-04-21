from typing import Dict, Set, Tuple
from pydantic import HttpUrl
from helpers.helpers import update_dict_with_new_data
from helpers.html_content_helpers import download_link_content, remove_known_links
from services.url_filtering_service import filter_relevant_links_using_title
from models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel, \
     UrlAnalysisInfoLinks
from services.data_extraction_service import extract_information_from_url


async def scrape_and_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    extracted_data: dict[str, str] = {key: "" for key in params.sought_data}
    links_to_visit: set[HttpUrl] = {params.url}

    visited_links = set()
    while len(links_to_visit) > 0:
        current_link = links_to_visit.pop()
        if current_link in visited_links:
            continue
        visited_links.add(current_link)

        # TODO: maybe do these two in parallel
        new_data: Dict[str, str] = await extract_information_from_url(params)
        extracted_data = update_dict_with_new_data(extracted_data, new_data)
        extracted_links: UrlAnalysisInfoLinks = await download_link_content(current_link)
        clean_extracted_links: UrlAnalysisInfoLinks = await remove_known_links(extracted_links, visited_links, links_to_visit)
        links_of_interest: Set[HttpUrl] = await filter_relevant_links_using_title(clean_extracted_links.link_dictionary, clean_extracted_links.titles_set, params.sought_data)
        new_links = links_of_interest
        links_to_visit.update(new_links)


    return UrlAnalysisResponseModel(extracted_data=extracted_data)
