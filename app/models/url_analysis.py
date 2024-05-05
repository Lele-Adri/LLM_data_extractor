from typing import List
from pydantic import BaseModel, HttpUrl, Field



class UrlAnalysisRequestParams(BaseModel):
    url: HttpUrl     = Field(..., description="The URL to extract data from.")
    sought_data: dict[str, str] = Field(...,
                             description="A dictionary where each key-value pair defines a specific data point to extract from the URL. \
                                            **Key**: Name of the field to look for. \
                                            **Value**: Description of the field. \
                                            *Example*: {'Investment strategy': 'The investment strategy of the firm, e.g., taking risks, big investments only.'}")


class ExtractedDataAndSource(BaseModel):
    """Extracted information about some data from some url."""
    data_name: str = Field(..., description="name of the extracted data.")
    data_description: str = Field(..., description="Description of the extracted data.")
    data_source: str = Field(..., description="Data source where data was extracted.")
    extracted_information: str = Field(..., description="Information extracted from the data source.")


class UrlAnalysisResponseModel(BaseModel):
    """Url analysis response model"""
    extracted_data: dict[str, List[ExtractedDataAndSource]] = Field(..., description="A dictionary containing extracted data")



