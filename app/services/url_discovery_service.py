import os
from typing import Dict, Set

import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from pydantic import HttpUrl
import requests
from app.app_constants import MAX_LINKS_TO_VISIT_ENVIRONMENT_VARIABLE_NAME
from app.domain.url_analysis.entities import EmptyUrlAnalysisInfoLinks, UrlAnalysisDiscoveredLinks, UrlAnalysisInfoLinks
from app.helpers.url_analysis_helpers import normalize_url, set_contains_link
from app.models.url_analysis import UrlAnalysisRequestParams
from app.services.url_filtering_embeddings_service import filter_relevant_links_using_title

def remove_known_links(info_links: UrlAnalysisInfoLinks, visited_links: Set[str]) -> UrlAnalysisInfoLinks:
    info_links.link_dictionary = {url: title for url, title in info_links.link_dictionary.items()
                                  if not set_contains_link(visited_links, url)}
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
    MAX_LINKS_TO_VISIT = int(os.getenv(MAX_LINKS_TO_VISIT_ENVIRONMENT_VARIABLE_NAME, 5))
    while len(links_to_visit) > 0 and counter < MAX_LINKS_TO_VISIT:
        counter += 1
        print(f'counter: {counter}')
        current_link = links_to_visit.pop()
        print(f'visiting {current_link}')
        visited_links.add(current_link)
        extracted_links: UrlAnalysisInfoLinks = await get_exposed_urls(current_link)
        print(f'\textractedLinks: {len(extracted_links.link_dictionary)}')
        extracted_links = remove_known_links(extracted_links, visited_links)
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
    content = await fetch_url_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    links: Dict[str, str] = {
        urljoin(url, link['href']): str(link.string).strip(" \n ")
        for link in soup.find_all('a')[0:3]
        if link.get('href')
    }

    return UrlAnalysisInfoLinks(link_dictionary=links)

async def fetch_url_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as r:
                r.raise_for_status()
                return await r.text()

    except aiohttp.ClientError as e:
        print(f"Request exception occurred for url: {url} - {e}")
        return ""
    except Exception as e:
        print(f"Unknown error occurred for url: {url} - {e}")
        return ""
