from pydantic import BaseModel, HttpUrl, Field

class UrlAnalysisRequestParams(BaseModel):
    url: HttpUrl     = Field(..., description="The URL to extract data from.")
    sought_data: dict[str, str] = Field(...,
                             description="A dictionary where each key-value pair defines a specific data point to extract from the URL. \
                                            **Key**: Name of the field to look for. \
                                            **Value**: Description of the field. \
                                            *Example*: {'Investment strategy': 'The investment strategy of the firm, e.g., taking risks, big investments only.'}")


class UrlAnalysisResponseModel(BaseModel):
    """Url analysis response model"""
    extracted_data: dict = Field(..., description="A dictionary containing extracted data")

class UrlAnalysisInfoLinks(BaseModel):
    """Output from function download link content"""
    html_content: str = Field(..., description="HTML content of the webpage")
    link_dictionary: dict[str, str] = Field(..., description="Dictionary containing titles and urls of links")
    titles_set: set[str] =  Field(..., description="Set containing all the titles of the links")
    urls_set: set[HttpUrl] =  Field(..., description="Set containing all the urls of the links")
