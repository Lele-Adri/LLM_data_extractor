from typing import Dict, Set
from pydantic import HttpUrl
from app.helpers.helpers import update_dict_with_new_data
from app.helpers.html_content_helpers import download_link_content, normalize_url, remove_known_links, remove_out_of_scope_links
from app.services.url_filtering_embeddings_service import filter_relevant_links_using_title
from app.services.url_filtering_service import filter_relevant_links_using_embeddings

from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel, \
     UrlAnalysisInfoLinks
from app.services.data_extraction_service import extract_information_from_url, extract_information_and_sources_from_url

MAX_LINKS_TO_VISIT = 50

async def scrape_and_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    extracted_data: dict[str, str] = {key: "" for key in params.sought_data}

    links_to_visit: set[HttpUrl] = {params.url}

    treshold = 0.3

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
        print("\n Enter filtering method \n")
        print(clean_extracted_links.link_dictionary)
        links_of_interest: Set[HttpUrl] = await filter_relevant_links_using_embeddings(clean_extracted_links.link_dictionary, clean_extracted_links.titles_set, params.url, params.sought_data, treshold)
        print("\n Exit filtering method \n")
        print(links_of_interest)
        new_links = links_of_interest
        print("\n Before: \n")
        print(links_to_visit)
        links_to_visit.update(new_links)
        print("\n After: \n")
        print(links_to_visit)



    return UrlAnalysisResponseModel(extracted_data=extracted_data)

async def scrape_then_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    links_for_data_extraction: Set[str] = await discover_useful_links(params)
    return await extract_information_and_sources_from_url(params, links_for_data_extraction)

async def discover_useful_links(params: UrlAnalysisRequestParams) -> Set[str]:
    links_to_visit: set[str] = {normalize_url(str(params.url))}
    visited_links: set[str] = set()
    links_for_data_extraction: Set[str] = set()
    counter = 0
    while len(links_to_visit) > 0 and counter < MAX_LINKS_TO_VISIT:
        counter += 1
        print(f'counter: {counter}')
        current_link = links_to_visit.pop()
        print(f'visiting {current_link}')
        visited_links.add(current_link)
        extracted_links: UrlAnalysisInfoLinks = await download_link_content(current_link)
        print(f'\textractedLinks: {len(extracted_links.link_dictionary)}')
        extracted_links = remove_known_links(extracted_links, visited_links, links_to_visit)
        print(f'\textractedLinks (remove known): {len(extracted_links.link_dictionary)}')
        links_of_interest: set[str] = remove_out_of_scope_links(params.url, extracted_links.link_dictionary.keys())
        filtered_links_of_interest: set[str] = await filter_relevant_links_using_title(links_of_interest, params.sought_data)
        print(f'\tfiltered extractedLinks: {len(filtered_links_of_interest)}')
        visited_links.update(extracted_links.link_dictionary.keys() - filtered_links_of_interest)
        links_to_visit.update(filtered_links_of_interest)
        links_for_data_extraction.update(filtered_links_of_interest)
    return links_for_data_extraction
