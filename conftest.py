import pytest
import requests
from common_utility import read_config_file
import os

path_current_directory = os.path.dirname(__file__)
path_config_file = path_current_directory + '/commonconfig.ini'
config = read_config_file(path_config_file)
main_url = config['configuration_setting']['base_url']


# @pytest.fixture(scope="function",autouse=True)
# def print_funny_statment(request):
#     yield
#     if request.config.getoption('--may-force'):
#         print("“May the Force Be With You”")


@pytest.fixture(scope="function")
def search_in_resource():
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


first_test = []
flag_config = [False]

def pytest_collection_modifyitems(config, items):
    """
    Called after collection has been performed
    :param config:
    :param items:
    :return:
    """
    first_test.append(items[0])
    if config.getoption("--may-force"):
        flag_config[0] = True


def pytest_collection_finish():
    """
    Called after collection has been performed and modified.
    :return:
    """
    if flag_config[0]:
        print("Come To The Dark Side!")


def pytest_runtest_makereport(item, call):
    """
    Called to create a TestReport for each of the setup, call and teardown runtest phases of a test item.
    :param item:
    :param call:
    :return:
    """
    if call.when == 'call':
        if item == first_test[0]:
            if flag_config[0]:
                print('We have cookies!')

    elif call.when == 'teardown':
        if flag_config[0]:
            print('May the Force Be With You.')

def pytest_addoption(parser):
    parser.addoption("--may-force", action="store_true", default=False, help="The flag is required to print the statments ")