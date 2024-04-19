from fastapi import APIRouter
from typing import Tuple, Dict, Set, List
from pydantic import HttpUrl
from models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel,\
     UrlAnalysisInfoLinks
from services.url_analyzer_service import test_analyze_url, analyse_url, \
     download_link_content, filter_relevant_links_using_title

url_analysis_router = APIRouter(prefix="/url-analysis", tags=["URL Analysis"])

@url_analysis_router.post("")
async def analyze_url(request: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    """
    Analyzes the URL and extracts data as specified by the parameters.
    This could involve complex logic and further validations that are
    detailed here or in external services.

    Returns:
    - dict: A dictionary containing the data retrieved.
    """
    # Implementation of URL analysis would go here
    extractedData : UrlAnalysisResponseModel = await test_analyze_url(request)

    return extractedData


@url_analysis_router.post("/test_adri")
async def test_adri_url(request: UrlAnalysisRequestParams) -> Tuple[Set[str], Set[HttpUrl]]:
    """
    """
    test_data1 : UrlAnalysisInfoLinks = await download_link_content(request)

    #extracted_link_test = set(["https://www.mersen.com//group/mersen-group", \
    #    "https://www.mersen.com//group/corporate-social-responsibility", \
    #    "https://www.mersen.com//investors/mersen-profile"])

    test_data_2 : Tuple[Set[str], Set[HttpUrl]] = await filter_relevant_links_using_title(test_data1.link_dictionary, test_data1.titles_set, request.parameters)
    return test_data_2
