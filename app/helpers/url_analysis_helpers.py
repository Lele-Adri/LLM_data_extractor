from typing import Set
from urllib.parse import urlparse, urlunparse


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


def are_sections_of_same_page(url1: str, url2: str) -> bool:
    idx_hashtag_url1 = url1.find("#")
    idx_hashtag_url2 = url2.find("#")
    if idx_hashtag_url1 != -1:
        url1 = url1[:idx_hashtag_url1]
    if idx_hashtag_url2 != -1:
        url2 = url2[:idx_hashtag_url2]
    return url1 == url2


def set_contains_link(links_set: Set[str], url: str) -> bool:
    for link in links_set:
        if are_sections_of_same_page(link, url):
            return True
    return False
