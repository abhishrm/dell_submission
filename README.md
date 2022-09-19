# API specific to STAR WAR
Only test specific to endpoint /people are covered.

#Test framework structuring:
 1.conftest.py-> Contains all fixtures and hooks required for test placed in test_star_war_api.py.
 2.test_star_war_api.py -> This is the main test file which contains all the test related to star war API specific to "people" endpoint.
 3.commonconfig.ini-> This is an INI file from where some set of congiguration can be read for example urls.
 4.common_utility.py-> This contains all the common code which can be used at various places in the project.


## Summary i.e. what has been covered details mentioned below
This is a repository specifically written to verify [Star Wars API](https://swapi.py4e.com/documentation).  
It covers the folloiwng:  
1) create fixture that returns an array with all people
2) create test which checks that names of all people are unique
3) create test (or a few) with validation that search for people is case insensitive
4) create test which validates that there is no page with number 0 for people request 
5) create parametrized test which checks that there are 3 Skywalker's, 1 Vader, 2 Darth's (using 
?search)
6) create test(s) which validate that all people objects contain required schema fields.
If validation fails – person id and name should be in error/fail message.
All persons with failed validation must be reported during one test run.
7) create factory fixture “search_in_resource” that returns search function depending on the 
resource name provided as a parameter (people, planet, etc)
8) create test which checks that search for any char in English alphabet or any number from 0 to 9 
returns number of results>0 except cases of search by 6, 9 and 0. It is not allowed to use loops 
inside the test body.
9) "funny prints” (these prints should NOT be inside test function code) (see screenshot below with 
example) (tips to read: conftest file and well defined hooks:
https://docs.pytest.org/en/6.2.x/reference.html#hook-reference)
a. on each time of tests execution the following phrase should appear only 1 time on the 
beginning of tests log: “We have cookies!” (even if executing a few files or classes or 
only one test)
b. at the end of each test the phrase “May the Force Be With You” should appear in log
c. *add a boolean parameter “may-force” for pytest launch (pytest –may-force) that is 
false by default. If specified as True then phrases from a) and b) should be printed. If 
false – phrases should not be in the log.
d. **add a print of a phrase “Come To The Dark Side!” in the way that it should appear in 
log after “collected X item(s)” but before first test started
point с) (“may-force” parameter) still should work (enables print in log if specified) for 
that message as well
10) try to suggest and implement any other meaningful and suitable tests for "get /people" request
11) *implement a decorator that can be applied to each test and measure test time execution
a. decorator should print the time to the log and also save the time to the file created in 
results folder with file_name = test_name
b. **implement decorator in a way when it is possible to parametrize it and disable output 
to file lik@get_time(write_to_file=True/False)
def test_my_test(…)|
 …
12) * try to suggest (and implement if possible) any meaningful and suitable tests for "get /people" 
requests with parameter ?format=wookiee 
13) * There is some bug with implementation of Wookiee format. It would be great if you can find 
that and say a few words with your thoughts what is the root cause. Please write some kind of 
“Bug report” for issue found in the way how you would create that in bugtracker system.


#Meaningful test for "get/people"
1. Invalid UUID in path or query parameters
2. Unsupported methods for endpoints for GET call
3. Validation of status code
       -When resource i.e people do not exist , then result should be 404
       ->Create resource Get it, then delete it and then get it.
4.Verify various filter query to seek , by passing filters we should get respective people details
5.Validate complete schema structure including hyperlinks present in the json response.


#Bug found with implementaion of wookie format are listed below:

1
Description: API call with wookie format does not return error in wookie format.
Steps to reproduce:
When user calls below API
https://swapi.py4e.com/api/people/?page=0/?format=wookiee.

Expected Result:
Error Details should be in Wookiee format.

Current observation:
Error Details are in English Language format.

Severity:Low.
Priority:P4(Low).

2
Description: Schema not returned with wookie format when people API is called.
Steps to reproduce:
When user calls below API:
https://swapi.py4e.com/api/people/schema?format=wookiee.

Expectation:
We expect schema  should be in Wookie format.

Current observation:
As of now JSON schema appears with keys in English format.

Severity:Medium.
Priority:P2(important).


#HOW TO RUN TEST:
pytest -s -v --mayforce test_star_war_api.py

#To produce html result please run like below:
pytest -s -v --mayforce test_star_war_api.py --html=report.html
