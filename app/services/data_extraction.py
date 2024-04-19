import json
from operator import itemgetter
import os
from dotenv import load_dotenv
from typing import Dict
import html2text
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
import htmlmin
from pydantic import HttpUrl

from models.url_analysis import UrlAnalysisRequestParams


async def extract_information_from_url(params: UrlAnalysisRequestParams) -> Dict[str, str]:
    load_dotenv()
    llm = ChatOpenAI(
        temperature=0.1,
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        verbose=True,
        max_tokens=1000,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
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
