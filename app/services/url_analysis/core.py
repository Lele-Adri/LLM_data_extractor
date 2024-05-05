from typing import Set
from app.domain.url_analysis.entities import UrlAnalysisInfoLinks
from app.helpers.url_analysis_helpers import normalize_url
from app.services.url_analysis.utils import get_exposed_urls, remove_known_links, remove_out_of_scope_links
from app.services.url_filtering_embeddings_service import filter_relevant_links_using_title

from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel
from app.domain.url_analysis.entities import UrlAnalysisDiscoveredLinks
from app.services.data_extraction_service import extract_information_and_sources_from_url

MAX_LINKS_TO_VISIT = 5

async def scrape_then_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    links_for_data_extraction: UrlAnalysisDiscoveredLinks = await discover_useful_links(params)
    return await extract_information_and_sources_from_url(params, links_for_data_extraction)

async def discover_useful_links(params: UrlAnalysisRequestParams) ->  UrlAnalysisDiscoveredLinks:
    links_to_visit: Set[str] = {normalize_url(str(params.url))}
    visited_links: Set[str] = set()
    links_for_data_extraction: UrlAnalysisDiscoveredLinks = UrlAnalysisDiscoveredLinks(extracted_links={data: set() for data in params.sought_data.keys()})
    counter = 0
    while len(links_to_visit) > 0 and counter < MAX_LINKS_TO_VISIT:
        counter += 1
        print(f'counter: {counter}')
        current_link = links_to_visit.pop()
        print(f'visiting {current_link}')
        visited_links.add(current_link)
        extracted_links: UrlAnalysisInfoLinks = await get_exposed_urls(current_link)
        print(f'\textractedLinks: {len(extracted_links.link_dictionary)}')
        extracted_links = remove_known_links(extracted_links, visited_links, links_to_visit)
        print(f'\textractedLinks (remove known): {len(extracted_links.link_dictionary)}')
        links_of_interest: Set[str] = remove_out_of_scope_links(params.url, extracted_links.link_dictionary.keys())
        filtered_links_of_interest: UrlAnalysisDiscoveredLinks = await filter_relevant_links_using_title(links_of_interest, params.sought_data)
        print(f'\tfiltered extractedLinks: {len(filtered_links_of_interest.extracted_links)}')
        visited_links.update(extracted_links.link_dictionary.keys() - filtered_links_of_interest.get_all_links())
        links_to_visit.update(filtered_links_of_interest.get_all_links())
        links_for_data_extraction.updateFromDiscoveredLinks(filtered_links_of_interest)
    return links_for_data_extraction
