from app.helpers.url_analysis_helpers import set_contains_link


from typing import Set


class UrlAnalysisInfoLinks:
    """Output from function download link content"""
    def __init__(self, link_dictionary):
        self.link_dictionary: dict[str, str] = link_dictionary


class EmptyUrlAnalysisInfoLinks(UrlAnalysisInfoLinks):
    def __init__(self):
        super().__init__("", dict())


class UrlAnalysisDiscoveredLinks:
    """Object containing discovered links with each data piece as a key"""
    def __init__(self, extracted_links):
        self.extracted_links: dict[str, Set[str]] = extracted_links

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