
import os
from bs4 import BeautifulSoup
from pydantic import HttpUrl
import requests

from models.url_analysis import UrlAnalysisInfoLinks, UrlAnalysisRequestParams


def get_test_html_content():
    filename = "./static/atp_rankings.txt"
    full_path = os.path.abspath(filename)
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"


async def download_link_content_session(url: HttpUrl, use_test_file=False) -> str:
    if use_test_file:
        return get_test_html_content()
    try: 
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                  }
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url) # TODO: make async
        return response.text  
    except requests.RequestException as e:
        return str(e)  


# TODO: make async
async def download_link_content(params: UrlAnalysisRequestParams) -> UrlAnalysisInfoLinks:

    # extract links using BeautifulSoup
    r = requests.get(params.url)
    soup = BeautifulSoup(r.content, 'html.parser')

    links = soup.find_all("a") # Find all elements with the tag <a>

    title_link_dict = {}
    for link in links:
        href_link = str(link.get("href"))

        if href_link.startswith("http"):
            total_link = href_link
        else:
            total_link = str(params.url) + href_link

        title_link_dict[str(link.string).strip(" \n ")] = total_link

    # remove duplicate urls from dict
    cleaned_dict = {}
    for key,value in title_link_dict.items():
        if value not in cleaned_dict.values():
            cleaned_dict[key] = value

    # create list with titles and list with links frolm the dictionary
    title_list = []
    link_list = []
    for key, value in cleaned_dict.items():
        title_list.append(key)
        link_list.append(value)

    return UrlAnalysisInfoLinks(html_content=r.text,
                                link_dictionary=cleaned_dict,
                                titles_set=set(title_list),
                                urls_set=set(link_list))