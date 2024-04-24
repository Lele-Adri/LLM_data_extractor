
import os
from typing import Dict, Set
from urllib.parse import urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
from pydantic import HttpUrl
import requests

from models.url_analysis import UrlAnalysisInfoLinks, UrlAnalysisRequestParams


def get_test_html_content():
    filename = "./static/atp_rankings.txt"
    full_path = os.path.abspath(filename)
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"


async def download_link_content_session(url: HttpUrl, use_test_file=False) -> str:
    if use_test_file:
        return get_test_html_content()
    try:
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                  }
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url) # TODO: make async
        return response.text
    except requests.RequestException as e:
        return str(e)


# TODO: make async
async def download_link_content(url: str) -> UrlAnalysisInfoLinks:

    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    links: Dict[str, str] = {
        urljoin(url, link['href']): str(link.string).strip(" \n ")
        for link in soup.find_all('a')
        if link.get('href')
    }

    return UrlAnalysisInfoLinks(html_content=r.text, link_dictionary=links)


async def remove_known_links(info_links: UrlAnalysisInfoLinks, visited_links: Set[str], links_to_visit: Set[str]) -> UrlAnalysisInfoLinks:
    info_links.link_dictionary = {url: title for url, title in info_links.link_dictionary.items() 
                                  if url not in visited_links and url not in links_to_visit}
    return info_links

    
def remove_out_of_scope_links(base_url: HttpUrl, info_links: Set[str]) -> set[str]:
    return {link for link in info_links if are_same_base_domain(str(base_url), link)}
    
def are_same_base_domain(url1: str, url2: str) -> bool:
    urlparse(url2).netloc = urlparse(url1).netloc

def normalize_url(url: str):
    # Parse the URL into components
    parsed_url = urlparse(url)
    # Normalize the components
    normalized = parsed_url._replace(
        scheme=parsed_url.scheme.lower(),
        netloc=parsed_url.netloc.lower(),
        path=parsed_url.path.rstrip('/'),
        query=parsed_url.query,
        fragment=''
    )
    # Return the normalized URL as a string
    return urlunparse(normalized)
