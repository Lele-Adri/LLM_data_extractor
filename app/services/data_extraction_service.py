from typing import Dict, List, Set
from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from app.models.url_analysis import ExtractedDataModel, UrlAnalysisRequestParams, UrlAnalysisResponseModel
from app.helpers.llm_helpers import get_gpt_3

NOT_FOUND_STRING  = "NOT FOUND"

async def extract_information_and_sources_from_url(params: UrlAnalysisRequestParams, urls_set: Set[str]) -> UrlAnalysisResponseModel:
    if (len(urls_set) == 0): return dict()

    indexes: Dict[VectorstoreIndexCreator] = {url: VectorstoreIndexCreator().from_loaders([WebBaseLoader(url)]) for url in urls_set}
    response: UrlAnalysisResponseModel = UrlAnalysisResponseModel(
        extracted_data={data: set() for data in params.sought_data.keys()}
    )

    for data, description in params.sought_data.items():
        query = get_data_query(data, description)
        for url, index in indexes.items():
            ans = index.query(query)
            if NOT_FOUND_STRING not in ans and ans != "":
                response.extracted_data[data].append(
                    ExtractedDataModel(data_name=data,
                                       data_description=description,
                                       data_source=url,
                                       extracted_information=ans)
                )

    return response

async def extract_information_from_url(params: UrlAnalysisRequestParams, urls_list: List[str]) -> Dict[str, str]:
    if (len(urls_list) == 0): return dict()

    index = VectorstoreIndexCreator().from_loaders([WebBaseLoader(url) for url in urls_list])
    extracted_data_dict = dict()

    for data, description in params.sought_data.items():
        query = get_data_query(data, description)
        ans = index.query(query)
        if "NOT FOUND" not in ans and ans != "":
            extracted_data_dict[data] = f"{extracted_data_dict.get(data, '')}\n{ans}"

    return extracted_data_dict

def get_data_query(data: str, description: str):
        return f"""
                This is part of a larger application that allows users to extract information from web pages.
                The user has now specified the information they are interested in.
                Here is their input:
                    - [Data name]: {data}
                    - [Description]: {description}
                Your task is to look up this information from the provided web content.
                You should either output the information you gathered from the web content, or "{NOT_FOUND_STRING}" if you didn't find it.
                If you did find the information, only provide the information you found, without any additional comments.
                The answer should concise and straight to the point, while containing all the information you could find.
                """
