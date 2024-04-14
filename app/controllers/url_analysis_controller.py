from fastapi import APIRouter
from models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel
from services.url_analyzer_service import test_analyze_url, analyse_url


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