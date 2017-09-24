# Degree Analytics Coding Challenge

## Requirements:

Create a python flask/django API that shows a chart and data projection for the amount of Python and R Repos that will be created over the next 5 years on Github (use the github api for retrieving data)

## Setting up your local environment:

  Install virtualenv and pip before you proceed with the following steps:

    mkvirtualenv <name> # Create virtual environment
    lsvirtualenv # List the virtual environment

  In the activated python environment:

    pip install -r requirements.txt

  Run the script

    python app/main.py

  The test automation suit is built on [Pytest](https://docs.pytest.org/en/latest/). To test run...

    pytest

  After tests have been run the results can be viewed while the api is running with the Pytest here

    pytest --html=report.html

![Pytest-Report.png](./Pytest-Report.png)

## Documentation

  * [View API Documentation](https://documenter.getpostman.com/view/1959462/degree_analytics_coding_challenge/6thy1NH)
