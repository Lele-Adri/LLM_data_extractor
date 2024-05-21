from typing import Dict, List, Set, Tuple
from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from app.models.url_analysis import ExtractedDataAndSource
from app.models.url_analysis import UrlAnalysisRequestParams, UrlAnalysisResponseModel
from app.helpers.llm_helpers import get_gpt_3
from app.domain.url_analysis.entities import UrlAnalysisDiscoveredLinks

NOT_FOUND_STRING  = "NOT FOUND"

async def extract_information_and_sources_from_url_list(sought_data: Dict[str, str], discovered_urls: UrlAnalysisDiscoveredLinks) -> UrlAnalysisResponseModel:

    response: UrlAnalysisResponseModel = UrlAnalysisResponseModel(
        extracted_data={data: set() for data in discovered_urls.extracted_links.keys()})

    for data, discovered_urls_set in discovered_urls.extracted_links.items():
        for url in discovered_urls_set:
            extracted_data = await extract_information_and_sources_from_url(url, (data, sought_data[data]))
            if extracted_data:
                response.extracted_data[data].append(extracted_data)

    return response


async def extract_information_and_sources_from_url(url: str, data: Tuple[str, str]) -> ExtractedDataAndSource:
    (sought_data_name, sought_data_description) = data
    index = await VectorstoreIndexCreator().afrom_loaders([WebBaseLoader(url)])
    query = get_data_query(sought_data_name, sought_data_description)
    ans = await index.aquery(query)
    if NOT_FOUND_STRING not in ans and ans != "":
        return ExtractedDataAndSource(data_name=sought_data_name,
                                      data_description=sought_data_description,
                                      data_source=url,
                                      extracted_information=ans)
    return None


async def extract_information_from_url(params: UrlAnalysisRequestParams, urls_list: List[str]) -> Dict[str, str]:
    if (len(urls_list) == 0): return dict()

    index = await VectorstoreIndexCreator().afrom_loaders([WebBaseLoader(url) for url in urls_list])
    extracted_data_dict = dict()

    for data, description in params.sought_data.items():
        query = get_data_query(data, description)
        ans = await index.aquery(query)
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
