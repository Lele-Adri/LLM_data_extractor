from typing import Set
from typing import Dict, Set
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pydantic import HttpUrl
import requests

from app.domain.url_analysis.entities import UrlAnalysisInfoLinks, EmptyUrlAnalysisInfoLinks
from app.helpers.url_analysis_helpers import set_contains_link



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


def remove_known_links(info_links: UrlAnalysisInfoLinks, visited_links: Set[str], links_to_visit: Set[str]) -> UrlAnalysisInfoLinks:
    info_links.link_dictionary = {url: title for url, title in info_links.link_dictionary.items()
                                  if not set_contains_link(visited_links, url) and not set_contains_link(links_to_visit, url)}
    return info_links


def remove_out_of_scope_links(base_url: HttpUrl, info_links: Set[str]) -> Set[str]:
    return {link for link in info_links if are_same_base_domain(str(base_url), link)}


def are_same_base_domain(url1: str, url2: str) -> bool:
    return urlparse(url2).netloc == urlparse(url1).netloc

