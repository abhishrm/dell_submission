import pytest
import requests
from common_utility import read_config_file
import os

path_current_directory = os.path.dirname(__file__)
path_config_file = path_current_directory + '/commonconfig.ini'
config = read_config_file(path_config_file)
main_url = config['configuration_setting']['base_url']


@pytest.fixture(scope="function",autouse=True)
def print_funny_statment(request):
    yield
    if request.config.getoption('--mayforce'):
        print("“May the Force Be With You”")


@pytest.fixture(scope="module",autouse=True)
def print_cookies(request):
    """
    This fixture is implemented at module level so that we can print statment before the start of the test
    :return:
    """
    if request.config.getoption('--mayforce'):
        print("“We have cookies!” ")


@pytest.fixture
def search_in_resource(scope="session"):
    def resource_search_response(resource,query_string):
        url_to_call = main_url +resource + "/?search=" + query_string
        response = requests.get(url_to_call)
        return response
    return resource_search_response

@pytest.fixture
def test_get_employee_details_check_status_code_equals_200():
     """
     Thi is a  fixture that returns an array with all people and response content as dict of the API call.
     :return: tuple
     """
     url_to_call = main_url + 'people/'
     response = requests.get(url_to_call)
     assert response.status_code == 200, "API call failed due to unexpected error code :{}".format(response.status_code)

     read_data_as_dict = response.json()

     no_of_names_find_under_get_call = [key["name"] for key in read_data_as_dict["results"] ]
     return no_of_names_find_under_get_call,read_data_as_dict

def pytest_addoption(parser):
    parser.addoption("--mayforce", action="store_true", default=False, help="Based on gthis flag we enable or disable prints")
