from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel
from app.domain.url_analysis.entities import UrlAnalysisDiscoveredLinks
from app.services.data_extraction_service import extract_information_and_sources_from_url_list
from app.services.url_discovery_service import discover_useful_links


async def scrape_then_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    links_for_data_extraction: UrlAnalysisDiscoveredLinks = await discover_useful_links(params)
    return await extract_information_and_sources_from_url_list(params.sought_data, links_for_data_extraction)
