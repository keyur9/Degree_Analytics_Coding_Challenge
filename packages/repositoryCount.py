"""This module will get the count of the repository."""

from flask import Flask
from dateutil.relativedelta import relativedelta
import requests
import dateutil.parser as parser
import logging
import imp
# Importing global module
globalVariable = imp.load_source('*', './app/global.py')
# Place where app is defined
app = Flask(__name__, template_folder=globalVariable.tmplDir)


class Repository(object):
    """
    Repository have the following properties.

    Attributes:
        year: A year in which the repositories are created.
        count: A total number of the repositories created for
                the language in a year.
    """

    def __init__(self, year, count):
        """
        Return a Repository object.

        Where current year is *year* and total number of repositories
        is *count*.
        """
        self.year = year
        self.count = count


def getRepositoryCount(language):
    """
    Function calling Github API to get the number of repository by year.

    Parameters:
    language - The language for which we want to fetch the repository count.

    Return -
    repositoryCount - List of current repository count
    """
    # Start date to fetch the data
    start_date = globalVariable.startDate
    # Fetch the data till date which is 10 years from start date
    end_date = start_date + relativedelta(years=globalVariable.relativeDeltaEndDate)
    # List for storing the respone
    repositoryCount = []
    # Loop to request and store data of the number of repositories
    # created in a year
    while start_date < end_date:
        # Incrementing date to get data by year
        start_date = start_date + relativedelta(years=globalVariable.relativeDeltaYear)
        # Generating query string based on the search request
        url = globalVariable.baseURL + language + globalVariable.queryFilter + start_date.strftime('%Y')
        # Trying to pull the data from the api
        try:
            # Sending request for the specific url
            r = requests.get(url)
            # Response from the above request
            response_dict = r.json()
            # Check to see if receive any response
            if response_dict is None:
                # Raising exception as received None in the response
                raise TypeError(globalVariable.raiseTypeErrorMessage)
            # Store data as received response
            else:
                # Storing the partial response in the list
                repositoryCount.append(Repository(parser.parse(start_date.strftime('%Y')).year, response_dict[globalVariable.responseKeyTotalCount]))
        # Catching TypeError
        except TypeError:
            app.logger.error(globalVariable.handleTypeErrorMessage)
            break
        # Catching KeyError
        except KeyError:
            # Logging error message if Key['total_count']
            # is not found in the response
            app.logger.error(response_dict[globalVariable.responseKeyMessage])
            pass
        # Catching ConnectionError
        except requests.exceptions.ConnectionError:
            # Logging error message if not connected to the Internet
            app.logger.error(globalVariable.networkConnectionError)
        # Catching TimeoutError
        except requests.exceptions.Timeout as err:
            # Logging error message if the Internet connection is slow
            app.logger.error(err)
    # Returning the object
    return repositoryCount
