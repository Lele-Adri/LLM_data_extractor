from typing import Dict, List
from fastapi.testclient import TestClient
from app.main import app
from app.models.url_analysis import UrlAnalysisRequestParams
from tests.input_cases_enums import SoughtData

client = TestClient(app)

def post_to_url_analysis(url: str, sought_data: Dict[str, str]):
    """Helper function to send a POST request to the url-analysis endpoint."""
    response = client.post(
        "/url-analysis",
        json={"url": url, "sought_data": sought_data},
    )
    return response


def post_to_url_analysis_RequestParams(params: UrlAnalysisRequestParams):
    """Helper function to send a POST request to the url-analysis endpoint."""
    response = client.post(
        "/url-analysis",
        json=params.model_dump_json(),
    )
    return response


def get_sought_data_dict(sought_data_types: List[SoughtData]) -> Dict[str, str]:
    return {sd.name: sd.description for sd in sought_data_types}


 