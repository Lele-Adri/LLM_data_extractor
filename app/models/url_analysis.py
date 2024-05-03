from typing import List
from pydantic import BaseModel, HttpUrl, Field

class UrlAnalysisRequestParams(BaseModel):
    url: HttpUrl     = Field(..., description="The URL to extract data from.")
    sought_data: dict[str, str] = Field(...,
                             description="A dictionary where each key-value pair defines a specific data point to extract from the URL. \
                                            **Key**: Name of the field to look for. \
                                            **Value**: Description of the field. \
                                            *Example*: {'Investment strategy': 'The investment strategy of the firm, e.g., taking risks, big investments only.'}")


class ExtractedDataModel(BaseModel):
    """Extracted information about some data."""
    data_name: str = Field(..., description="Name of extracted data.")
    data_description: str = Field(..., description="Description of extracted data.")
    data_source: str = Field(..., description="Source of extracted data.")
    extracted_information: str = Field(..., description="Information extracted corresponding to this data.")


class UrlAnalysisResponseModel(BaseModel):
    """Url analysis response model"""
    extracted_data: dict[str, List[ExtractedDataModel]] = Field(..., description="A dictionary containing extracted data")


class UrlAnalysisInfoLinks(BaseModel):
    """Output from function download link content"""
    html_content: str = Field(..., description="HTML content of the webpage")
    link_dictionary: dict[str, str] = Field(..., description="Dictionary containing titles and urls of links")

class EmptyUrlAnalysisInfoLinks(UrlAnalysisInfoLinks):
    html_content: str = ""
    link_dictionary: dict[str, str] = {}