from fastapi import APIRouter
from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel

from app.services.url_analyzer_service import scrape_then_extract_data


url_analysis_router = APIRouter(prefix="/url-analysis", tags=["URL Analysis"])

# Endpoint for https://your-domain.com/
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
    # Implementation of URL analysis would go here
    extractedData : UrlAnalysisResponseModel = await scrape_then_extract_data(request)
    return extractedData


@url_analysis_router.post("/test_adri")
async def test_adri_url(request: dict) -> str:
    """
    """
    name_1 = request["nom"]
    name_2 = request["quality"]

    return name_1 + " is very " + name_2
