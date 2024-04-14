from pydantic import BaseModel, HttpUrl, Field

class UrlAnalysisRequestParams(BaseModel):
    url: HttpUrl     = Field(..., description="The URL to extract data from.")
    parameters: dict = Field(...,
                             description="A dictionary where each key-value pair defines a specific data point to extract from the URL. \
                                            **Key**: Name of the field to look for. \
                                            **Value**: Description of the field. \
                                            *Example*: {'Investment strategy': 'The investment strategy of the firm, e.g., taking risks, big investments only.'}")


class UrlAnalysisResponseModel(BaseModel):
    """Url analysis response model"""
    extracted_data: dict = Field(..., description="A dictionary containing extracted data")