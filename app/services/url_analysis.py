from typing import Dict, Set

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from pydantic import HttpUrl
import requests
from app.domain.url_analysis.entities import EmptyUrlAnalysisInfoLinks, UrlAnalysisInfoLinks
from app.helpers.url_analysis_helpers import normalize_url, set_contains_link
from app.services.url_filtering_embeddings_service import filter_relevant_links_using_title

from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel
from app.domain.url_analysis.entities import UrlAnalysisDiscoveredLinks
from app.services.data_extraction_service import extract_information_and_sources_from_url

MAX_LINKS_TO_VISIT = 5

async def scrape_then_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    links_for_data_extraction: UrlAnalysisDiscoveredLinks = await discover_useful_links(params)
    return await extract_information_and_sources_from_url(params, links_for_data_extraction)


def remove_known_links(info_links: UrlAnalysisInfoLinks, visited_links: Set[str], links_to_visit: Set[str]) -> UrlAnalysisInfoLinks:
    info_links.link_dictionary = {url: title for url, title in info_links.link_dictionary.items()
                                  if not set_contains_link(visited_links, url) and not set_contains_link(links_to_visit, url)}
    return info_links


def are_same_base_domain(url1: str, url2: str) -> bool:
    return urlparse(url2).netloc == urlparse(url1).netloc


def remove_out_of_scope_links(base_url: HttpUrl, info_links: Set[str]) -> Set[str]:
    return {link for link in info_links if are_same_base_domain(str(base_url), link)}

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


# TODO: make async
async def get_exposed_urls(url: str) -> UrlAnalysisInfoLinks:

    try:
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                    }
        session = requests.Session()
        session.headers.update(headers)
        r = session.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Request exception occurred for url: {url}")
        return EmptyUrlAnalysisInfoLinks()
    except:
        print(f"Unknown error occurred for url: {url}")
        return EmptyUrlAnalysisInfoLinks()


    links: Dict[str, str] = {
        urljoin(url, link['href']): str(link.string).strip(" \n ")
        for link in soup.find_all('a')
        if link.get('href')
    }

    return UrlAnalysisInfoLinks(link_dictionary=links)

