"""Module for testing API."""
import imp
import requests
module = imp.load_source('*', './app/helpers.py')

"""
Few tests, will definitely add more test in future...
"""


def test_compare_language():
    """Function to test for the supported language."""
    test_input = 'Python'
    test_input1 = 'R'
    test_input2 = 'Java'
    assert module.compare_language(test_input) == True
    assert module.compare_language(test_input2) == False
    assert module.compare_language(test_input1) == True


def broken_function():
    """Function to raise Exception."""
    raise Exception('This is broken')


def test_connection():
    """Function to test connection."""
    try:
        r = requests.get('https://www.google.com')
    except requests.exceptions.ConnectionError:
        with assertRaises(Exception) as context:
            broken_function()
        assertTrue('This is broken' in str(exception))
