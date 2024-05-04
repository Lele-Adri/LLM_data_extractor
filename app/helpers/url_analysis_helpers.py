from pydantic import BaseModel, Field


class UrlAnalysisInfoLinks(BaseModel):
    """Output from function download link content"""
    html_content: str = Field(..., description="HTML content of the webpage")
    link_dictionary: dict[str, str] = Field(..., description="Dictionary containing titles and urls of links")


class EmptyUrlAnalysisInfoLinks(UrlAnalysisInfoLinks):
    html_content: str = ""
    link_dictionary: dict[str, str] = {}



class ExtractedDataModel(BaseModel):
    """Extracted information about some data."""
    data_name: str = Field(..., description="Name of extracted data.")
    data_description: str = Field(..., description="Description of extracted data.")
    data_source: str = Field(..., description="Source of extracted data.")
    extracted_information: str = Field(..., description="Information extracted corresponding to this data.")
