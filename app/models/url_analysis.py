from typing import List, Set
from pydantic import BaseModel, HttpUrl, Field

from app.helpers.html_content_helpers import set_contains_link
from app.helpers.url_analysis_helpers import ExtractedDataModel

class UrlAnalysisRequestParams(BaseModel):
    url: HttpUrl     = Field(..., description="The URL to extract data from.")
    sought_data: dict[str, str] = Field(...,
                             description="A dictionary where each key-value pair defines a specific data point to extract from the URL. \
                                            **Key**: Name of the field to look for. \
                                            **Value**: Description of the field. \
                                            *Example*: {'Investment strategy': 'The investment strategy of the firm, e.g., taking risks, big investments only.'}")


class UrlAnalysisResponseModel(BaseModel):
    """Url analysis response model"""
    extracted_data: dict[str, List[ExtractedDataModel]] = Field(..., description="A dictionary containing extracted data")


class UrlAnalysisDiscoveredLinks(BaseModel):
    """Object containing discovered links with each data piece as a key"""
    extracted_links: dict[str, Set[str]] = Field(..., description="A dictionary containing extracted data")

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

