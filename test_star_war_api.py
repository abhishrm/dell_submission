import pytest
import requests
import random
import os
from common_utility import *

path_current_directory = os.path.dirname(__file__)
path_config_file = path_current_directory + '/commonconfig.ini'
config = read_config_file(path_config_file)
main_url = config['configuration_setting']['base_url']



class Test():

    @get_time(write_to_file=True)
    def test_to_identify_unique_names(self,test_get_employee_details_check_status_code_equals_200):
        """
        Verify that names of all people are unique.
        :param test_get_employee_details_check_status_code_equals_200:
        :return:
        """
        assert len(test_get_employee_details_check_status_code_equals_200[0]) == len(set(test_get_employee_details_check_status_code_equals_200[0])),"Names are not unique as length is Not equal {}, {}".format(len(test_get_employee_details_check_status_code_equals_200[0]),len(set(test_get_employee_details_check_status_code_equals_200[0])))

    @get_time(write_to_file=True)
    def test_verify_search_for_people_is_case_insensitive(self, test_get_employee_details_check_status_code_equals_200):
        """
        Verify that search works with case insensitive
        :param test_get_employee_details_check_status_code_equals_200:
        :return:
        """
        case_insensitive_flag = None
        response_text = test_get_employee_details_check_status_code_equals_200[1]

        all_values = [ dict_get["name"] for dict_get in response_text["results"] ]
        case_insensitive_string_selected_randomly = random.choice(all_values)
        store_previous_default_value = case_insensitive_string_selected_randomly

        if case_insensitive_string_selected_randomly.isupper():
            case_insensitive_string_selected_randomly = case_insensitive_string_selected_randomly.lower()

        elif case_insensitive_string_selected_randomly.islower():
            case_insensitive_string_selected_randomly = case_insensitive_string_selected_randomly.upper()

        else:
            case_insensitive_string_selected_randomly = random.choice([case_insensitive_string_selected_randomly.upper(), case_insensitive_string_selected_randomly.lower()])

        url_formed = main_url + "/people/?search=" + case_insensitive_string_selected_randomly
        response = requests.get(url_formed)
        result_response = response.json()

        for dict_received in result_response["results"]:
            if store_previous_default_value in  dict_received.values():
                case_insensitive_flag = True
                break

        if case_insensitive_flag is not True:
            assert False, "Not able to perform case insenstive search for a random text :{} which exist in the system".format(case_insensitive_string_selected_randomly)


    @get_time(write_to_file=True)
    def test_verify_there_is_no_page_number_for_people_request(self):
        """
        Verify that there is no page with number 0 for people request
        :return:
        """
        url_formed = main_url + "people?page=0"
        response = requests.get(url_formed)

        assert response.status_code == 404 ,"Expected response code is 404 but received is :{} when endpoint is called with page 0".format(response.status_code)

    @get_time(write_to_file=True)
    @pytest.mark.parametrize("test_input,expected", [("Skywalker", 3), ("Vader", 1), ("Darth", 2)])
    def test_search(self,test_input,expected):
        """
         Verify that that there are 3 Skywalker's, 1 Vader, 2 Darth's (using?search)
        :param test_input:
        :param expected:
        :return:
        """
        url_formed = main_url +"/people/?search=" + test_input
        response = requests.get(url_formed)
        read_data_as_dict = response.json()

        no_of_names_find_under_get_call = [key["name"] for key in read_data_as_dict["results"] ]
        assert len(no_of_names_find_under_get_call) == expected,"Not matched search for string :{} under response :{}".format(expected,len(no_of_names_find_under_get_call))

    @get_time(write_to_file=True)
    def test_verify_schema_field(self):
        """
        Verify that all people objects contain required schema fields.
        If validation fails – person id and name should be in error/fail message.
        All persons with failed validation must be reported during one test run.
        :return:
        """
        url = main_url + "people/"
        response = requests.get(url)
        reference_schema_structure= ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'films', 'species', 'vehicles', 'starships', 'created', 'edited', 'url']
        for list_element in response.json()["results"]:

            if set(list_element.keys()) != set(reference_schema_structure):
                print ("Validation failed for person with name as :{}".format(list_element["name"]))
                assert False, "Schema validation failed as these two set are different, expected:{},received:{}".format(reference_schema_structure, list_element.keys())

   # @pytest.mark.parametrize("test_input,expected", [("Skywalker", 3), ("Vader", 1), ("Darth", 2)])
    @pytest.mark.parametrize("resource", ['people', 'planets', 'films', 'species', 'vehicles', 'starships'])
    def test_search_in_resource(self,resource, search_in_resource):
        """
        Test to create factory fixture “search_in_resource” that returns search function depending on the resource name provided as a parameter (people, planet, etc)
        :param search_in_resource:
        :return:
        """
        print(search_in_resource)

    @pytest.mark.parametrize('resource', ['people'])
    def test_swapi_resource_search_query_random(self,resource,search_in_resource):
        """
        Verify that search for any char in English alphabet or any number from 0 to 9 returns number of results>0 except cases of search by 6, 9 and 0
        :param search_in_resource:
        :return:
        """
        number_or_english_alphabet = generate_string_of_alpha_numeric_char()
        number_or_english_alphabet = number_or_english_alphabet[0:1]
        response = search_in_resource(resource, number_or_english_alphabet).json()

        if resource in ['people'] and number_or_english_alphabet in ['0', '6', '9']:
            assert len(response["results"]) == 0
        else:
            assert len(response["results"]) > 0

#  10) try to suggest and implement any other meaningful and suitable tests for "get /people" request
#Below test we can verify:
    # Invalid UUID in path or query parameters
    # Unsupported methods for endpoints for GET call
    # Validation of status code
      # -When resource i.e people do not exist , then result should be 404
      # ->Create resource Get it, then delete it and then get it
    #Verify various filter query to seek , by passing filters we should get respective people details
    #Validate complete schema structure including hyperlinks present in the json response.


# 12) * try to suggest (and implement if possible) any meaningful and suitable tests for "get /people" requests with parameter ?format=wookiee

#For Functional point of view we can verify below test:
# Verify the respective calls with different supported,unsupported format and then verify expected status code.
#Verify the different filter query supported.

# Invalid UUID in path or query parameters

# Unsupported methods for endpoints for GET call

    # Validation of status code
    # -When resource i.e people do not exist , then result should be 404
    # ->Create resource Get it, then delete it and then get it


