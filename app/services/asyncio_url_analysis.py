import os
import asyncio
from typing import Dict, Set, Tuple
from app.app_constants import MAX_LINKS_TO_VISIT_ENVIRONMENT_VARIABLE_NAME
from app.helpers.url_analysis_helpers import normalize_url
from app.models.url_analysis import ExtractedDataAndSource, UrlAnalysisRequestParams, UrlAnalysisResponseModel
from app.domain.url_analysis.entities import UrlAnalysisInfoLinks
from app.services.data_extraction_service import extract_information_and_sources_from_url
from app.services.url_discovery_service import get_exposed_urls, remove_known_links, remove_out_of_scope_links

from app.services.url_filtering_embeddings_service import is_url_relevant_for_data


results_queue = asyncio.Queue()
links_to_visit_queue = asyncio.Queue()
MAX_LINKS_TO_VISIT = int(os.getenv(MAX_LINKS_TO_VISIT_ENVIRONMENT_VARIABLE_NAME, 5))
TIMEOUT = 50

async def scrape_and_extract_data(params: UrlAnalysisRequestParams) -> UrlAnalysisResponseModel:
    await links_to_visit_queue.put(normalize_url(str(params.url)))
    visited_links = set()
    counter = 0
    filter_and_extract_tasks = create_filter_and_extract_task_for_data(str(params.url), params.sought_data) # TODO: should this be a set instead?
    tasks_are_running = True

    print("Entering main loop...")
    while counter < MAX_LINKS_TO_VISIT and (not links_to_visit_queue.empty() or tasks_are_running): 
        print("Begin main loop...")
        
        while links_to_visit_queue.empty():
            _, pending = await asyncio.wait(filter_and_extract_tasks, return_when=asyncio.FIRST_COMPLETED, timeout=1)
            if pending:
                filter_and_extract_tasks = list(pending)
                await asyncio.sleep(1)
                continue
            else:
                tasks_are_running = False
                break

        if (not tasks_are_running and links_to_visit_queue.empty()): # Can this all be simplified? 
            break;

        current_link = await links_to_visit_queue.get()

        if not current_link or current_link in visited_links:
            print("Invalid link")
            continue
        counter += 1
        visited_links.add(current_link)
        extracted_links: UrlAnalysisInfoLinks = await get_exposed_urls(current_link)
        print(f"Number of extracted links: {len(extracted_links.link_dictionary)}")
        extracted_links = remove_known_links(extracted_links, visited_links)
        links_of_interest: Set[str] = remove_out_of_scope_links(params.url, extracted_links.link_dictionary.keys())
        filter_and_extract_tasks.extend(create_filter_and_extract_task(links_of_interest, params.sought_data))

    print("Finished main loop, gathering tasks...")
    await asyncio.gather(*filter_and_extract_tasks)
    print("Finished gathering tasks, gathering results...")

    response: UrlAnalysisResponseModel = UrlAnalysisResponseModel(
        extracted_data = {data: [] for data in params.sought_data.keys()})
    while not results_queue.empty():
        result: ExtractedDataAndSource = await results_queue.get()
        if result:
            response.extracted_data[result.data_name].append(result)

    print("Finished gathering results, returning!")

    return response



def create_filter_and_extract_task(links_of_interest: Set[str], sought_data: Dict[str, str]):
    print("Creating tasks batch...")
    return [
        task
        for url in links_of_interest
        for task in create_filter_and_extract_task_for_data(url, sought_data)
    ]

def create_filter_and_extract_task_for_data(url: str, sought_data: Dict[str, str]):
    return [asyncio.create_task(process_url(url, sought_data_tuple))
            for sought_data_tuple in sought_data.items()]


async def process_url(url: str, sought_data_tuple: Tuple[str, str]):
    print(f"Processing url: {url}")
    if (await is_url_relevant_for_data(url, sought_data_tuple)):
        print(f"Passed filtering: {url}")
        await links_to_visit_queue.put(url)
        data_and_source: ExtractedDataAndSource = await extract_information_and_sources_from_url(url, sought_data_tuple)
        await results_queue.put(data_and_source)
    print(f"Finished Processing url: {url}")


def remain_running_tasks(tasks_list) -> bool:
    return any([task for task in tasks_list if not task.done()]) 