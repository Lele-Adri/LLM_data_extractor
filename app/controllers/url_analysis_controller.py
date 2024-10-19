from fastapi import APIRouter
from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel

from app.services.url_analysis import scrape_then_extract_data


url_analysis_router = APIRouter(prefix="/url-analysis", tags=["URL Analysis"])

@url_analysis_router.get("/hello")
def root():
    return {
        'message': "Hi, The API is running!"
    }


@url_analysis_router.post("/")
async def analyze_url(request: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    """
    Analyzes the URL and extracts data as specified by the parameters.
    This could involve complex logic and further validations that are
    detailed here or in external services.

    Returns:
    - dict: A dictionary containing the data retrieved.
    """
    extractedData : UrlAnalysisResponseModel = await scrape_then_extract_data(request)
    return extractedData
