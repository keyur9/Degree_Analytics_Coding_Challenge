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

    python main.py

  The test automation suit is built on [Pytest](https://docs.pytest.org/en/latest/). To test run...

    pytest

  After tests have been run the results can be viewed while the api is running with the Pytest here

    pytest --html=report.html

![Pytest-Report.png](./Pytest-Report.png)

## Documentation

  * [View API Documentation](https://documenter.getpostman.com/view/1959462/degree_analytics_coding_challenge/6thy1NH)

## Deployment using Docker

Install Docker before you proceed with the following steps:

    docker build -t degreeAnalytics . && docker run -it degreeAnalytics

## Example of repository data charts and projection for R language

Current repository data charts for R language

![Data-Charts.png](./Data-Charts.png)

Projection of number of repository that will be created for R language in next 5 years

![Data-Projection.png](./Data-Projection.png)
(Please hover over the labels to view the data points when running the application.)
