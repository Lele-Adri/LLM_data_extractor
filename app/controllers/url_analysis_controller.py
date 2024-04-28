from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Tuple, Set
from pydantic import HttpUrl
from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel,\
     UrlAnalysisInfoLinks
from app.services.url_analyzer_service import scrape_and_extract_data, \
                download_link_content, filter_relevant_links_using_title


#url_analysis_router = APIRouter(prefix="/url-analysis", tags=["URL Analysis"])
url_analysis_api = FastAPI()

url_analysis_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Endpoint for https://your-domain.com/
@url_analysis_api.get("/")
def root():
    return {
        'message': "Hi, The API is running!"
    }


@url_analysis_api.post("/url-analysis")
async def analyze_url(request: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    """
    Analyzes the URL and extracts data as specified by the parameters.
    This could involve complex logic and further validations that are
    detailed here or in external services.

    Returns:
    - dict: A dictionary containing the data retrieved.
    """
    # Implementation of URL analysis would go here
    extractedData : UrlAnalysisResponseModel = await scrape_and_extract_data(request)
    return extractedData


@url_analysis_api.post("/test_adri")
async def test_adri_url(request: dict) -> str:
    """
    """
    name_1 = request["nom"]
    name_2 = request["quality"]

    return name_1 + " is very " + name_2
