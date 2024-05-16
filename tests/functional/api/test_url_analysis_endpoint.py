from typing import Dict

from tests.input_cases_enums import UrlSource, SoughtData
from benchmarks.profiler import profiled_test
from tests.utils import get_sought_data_dict, post_to_url_analysis

def test_url_analysis_valid_empty_data():
    url: str = UrlSource.ATP.url
    response = post_to_url_analysis(url, dict())
    assert response.status_code == 200

def test_url_analysis_invalid_empty_url():
    response = post_to_url_analysis("", dict())
    assert response.status_code == 422

def test_url_analysis_invalid_not_a_url():
    url: str = UrlSource.INVALID_URL.url
    response = post_to_url_analysis(url, dict())
    assert response.status_code == 422  

def test_url_analysis_invalid_None_data():
    url: str = UrlSource.ATP.url
    response = post_to_url_analysis(url, None)
    assert response.status_code == 422

@profiled_test
def test_single_specific_data():
    url: str = UrlSource.BAIN.url
    sought_data: Dict[str, str] = get_sought_data_dict([SoughtData.PARTNER_PROFILE])
    response = post_to_url_analysis(url, sought_data)
    assert response.status_code == 200

@profiled_test
def test_two_specific_unrelated_data():
    url: str = UrlSource.BAIN.url
    sought_data: Dict[str, str] = get_sought_data_dict([SoughtData.PARTNER_PROFILE, SoughtData.PRIMARY_AND_ADDON])
    response = post_to_url_analysis(url, sought_data)
    assert response.status_code == 200

@profiled_test
def test_two_same_data():
    url: str = UrlSource.GITHUB.url
    sought_data: Dict[str, str] = get_sought_data_dict([SoughtData.PERSONAL_DATA_COLLECTION, SoughtData.PERSONAL_DATA_COLLECTION])
    response = post_to_url_analysis(url, sought_data)
    assert response.status_code == 200

def test_data_not_found():
    url: str = UrlSource.GITHUB.url
    sought_data: Dict[str, str] = get_sought_data_dict([SoughtData.AGE_KYRGIOS])
    response = post_to_url_analysis(url, sought_data)
    assert response.status_code == 200

def test_found_not_found_data_combination():
    url: str = UrlSource.GITHUB.url
    sought_data: Dict[str, str] = get_sought_data_dict([SoughtData.PERSONAL_DATA_COLLECTION, SoughtData.AGE_KYRGIOS])
    response = post_to_url_analysis(url, sought_data)
    assert response.status_code == 200

def test_answer_found_in_table():
    url: str = UrlSource.ITTF.url
    sought_data: Dict[str, str] = get_sought_data_dict([SoughtData.TOP_5_IN_RANKINGS])
    response = post_to_url_analysis(url, sought_data)
    assert response.status_code == 200


def test_complex_query():
    pass