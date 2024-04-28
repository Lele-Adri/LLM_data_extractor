import json
from typing import Dict
from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator

from app.models.url_analysis import UrlAnalysisRequestParams
from app.helpers.llm_helpers import get_gpt_3


async def extract_information_from_url(params: UrlAnalysisRequestParams) -> Dict[str, str]:

    llm = get_gpt_3()

    # TODO: arg list will be populated with elements of data_to_extract
    loader = WebBaseLoader(str(params.url))
    index = VectorstoreIndexCreator().from_loaders([loader])

    sought_data_str = '\n'.join(f"\t\t'{key}': {value}" for key, value in params.sought_data.items())
    query = f"""
            From the presented HTML content, extract the following information:
            {sought_data_str}
            You should output a json of key value pairs, where the key is the name of the data you want to extract and the value is the data you extracted
            (which is the information described in the values of the previous list entries).
            Leave the value of the entry blank if the data is not in the url.
            """
    ans = index.query(query)
    output_dict = json.loads(ans)
    return output_dict
