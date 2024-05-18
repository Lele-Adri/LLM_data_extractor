from collections import defaultdict
from dataclasses import dataclass, field
from app.helpers.url_analysis_helpers import set_contains_link


from typing import Dict, Set


@dataclass
class UrlAnalysisInfoLinks:
    """Output from function download link content"""
    link_dictionary: dict[str, str]


@dataclass
class EmptyUrlAnalysisInfoLinks(UrlAnalysisInfoLinks):
    def __init__(self):
        super().__init__(link_dictionary=dict())


@dataclass
class UrlAnalysisDiscoveredLinks:
    """Object containing discovered links with each data piece as a key"""
    extracted_links: Dict[str, Set[str]]


    def contains_url(self, url):
        """Checks if a url is contained in the dictionary"""
        for _, links in self.extracted_links.items():
            if set_contains_link(links, url):
                return True
        return False

    def get_all_links(self) -> Set[str]:
        all_links: Set[str] = set()
        for _, link_set in self.extracted_links.items():
            all_links.update(link_set)
        return all_links

    def updateFromDiscoveredLinks(self, other: 'UrlAnalysisDiscoveredLinks') -> bool:
        for data, urls in other.extracted_links.items():
            if data in self.extracted_links:
                self.extracted_links[data].update(urls)
            else:
                self.extracted_links[data] = urls
