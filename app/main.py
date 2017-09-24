# -*- coding: utf-8 -*-

"""
Created on Fri Sep 22 12:38:56 2017.
@author: keyur
 Python Flask API that shows a chart and data projection
 for the amount of Python and R Repos that will be created
 over the next 5 years on Github (use the github api for retrieving data)
"""

"""# Import Modules"""
import os
from flask import Flask, render_template, Response, jsonify
from dateutil.relativedelta import relativedelta
import collections
import json
import requests
import dateutil.parser as parser
import logging
import datetime
import numpy as np
import imp
module = imp.load_source('*', './app/helpers.py')
globalVariable = imp.load_source('*', './app/global.py')

# Place where app is defined
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'templates')
app = Flask(__name__, template_folder=tmpl_dir)


"""Creting app.log file for logging purpose."""
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


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


def getProjectionRepositoryCount(count):
    """
    Projection of repositories for next n years.

    Parameters:
    count - List of current repositories count

    Return:
    predicted_years - List of predicted years
    predicted_count - List of predicted repositories count
    """
    # Value for how many number of years we want to predict?
    prediction_for_next_n_years = globalVariable.prediction_for_next_n_years
    # Starting date for the prediction
    start_year = globalVariable.start_year
    # Current data of repositories count for the language
    original_count = np.array(count)
    # Current data of years of repositories created
    original_years = np.array(range(1, len(original_count) + 1))
    # polyfit : Least squares polynomial fit.
    # Fitting the polynomial with 3rd degree
    curve_fit = np.polyfit(original_years, original_count, 3)
    # poly1d : A one-dimensional polynomial class.
    poly_fit = np.poly1d(curve_fit)
    # Identifying the range of prediction years
    predicted_years = np.append(original_years, list(range(max(original_years) + 1, max(original_years)+(prediction_for_next_n_years) + 1, 1)))
    # Adding data for
    predicted_years = predicted_years + start_year
    # Adding data for
    original_years = original_years + start_year
    # Creating list to store predicted values
    predicted_count = []
    # Loop to store the data of the number of repositories
    # created in the predicted years
    for i in range(0, len(predicted_years)):
        predicted_count.append(poly_fit(i + 1))
    # Returning the object
    return predicted_years, predicted_count


def getIndicativeMetrics(pred_years, pred_count):
    """
    Few indicative metrics.

    Parameters:
    pred_years - List of predicted years
    pred_count - List of predicted repositories count

    Return:
    chi2 - Estimate of error in the model
    chi2_red - Measure of goodness of fit
    s_err - Standard deviation of the error
    """
    # Storing the received data of predicted years
    years = np.array(pred_years)
    # Storing the received data of predicted number of repositories
    count = np.array(pred_count)

    # Modeling with Numpy
    # parameters and covariance from of the fit
    p, cov = np.polyfit(years, count, 3, cov=True)
    # model using the fit parameters; NOTE: parameters here are coefficients
    count_model = np.polyval(p, years)
    # Statistics
    # number of observations
    n = count.size
    # number of parameters
    m = p.size
    # degrees of freedom
    DF = n - m
    # Estimates of Error in Data/Model
    resid = count - count_model
    # chi-squared; estimates error in data
    chi2 = np.sum((resid/count_model)**2)
    # reduced chi-squared; measures goodness of fit
    chi2_red = chi2/(DF)
    # standard deviation of the error
    s_err = np.sqrt(np.sum(resid**2)/(DF))
    # Returning the object
    return chi2, chi2_red, s_err


def getRepositoryCount(language):
    """
    Function calling Github API to get the number of repository by year.

    Parameters:
    language - The language for which we want to fetch the repository count.

    Return -
    repositoryCount - List of current repository count
    """
    # urlCount = collections.OrderedDict()
    start_date = datetime.date(2008, 01, 01)
    # Fetch the data till date which is 10 years from start date
    end_date = start_date + relativedelta(years=10)
    # List for storing the respone
    repositoryCount = []
    # Loop to request and store data of the number of repositories
    # created in a year
    while start_date < end_date:
        # Incrementing date to get data by year
        start_date = start_date + relativedelta(years=1)
        # Generating query string based on the search request
        url = 'https://api.github.com/search/repositories?q=language:' + language + '+created:<' + start_date.strftime('%Y')
        # Trying to pull the data from the api
        try:
            # Sending request for the specific url
            r = requests.get(url)
            # Response from the above request
            response_dict = r.json()
            # Storing the partial response in the list
            repositoryCount.append(Repository(parser.parse(start_date.strftime('%Y')).year, response_dict['total_count']))
        except KeyError:
            # Logging error message if Key['total_count']
            # is not found in the response
            app.logger.error(response_dict['message'])
            pass
        except requests.exceptions.ConnectionError:
            # Logging error message if not connected to the Internet
            app.logger.error("We are not connected to the Internet, \
                            Let's connect to the internet and try agian")
        except requests.exceptions.Timeout as err:
            # Logging error message if the Internet connection is slow
            app.logger.error(err)
    # Returning the object
    return repositoryCount


@app.errorhandler(200)
def not_found(error=None):
    """Handling error in case of unexpected requests."""
    # Message to the user
    message = {
      "message": "Validation Failed",
      "errors": [
        {
          "message": "Current API support R and Python language search only."
        }
      ]
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 200
    # Returning the object
    return resp


@app.route("/api/v1.0/projection/<language>", methods=['GET'])
def index(language):
    """
    Function to show charts, perform data projection and render the charts.

    Parameters:
    language - The language for which we want to plot charts, predict for
    next n years and render the charts.
    """
    # Capturing user requested language
    _selectedlanguage = language
    # Checking if the requested language is supported in this version
    isLanguageAvailable = module.compare_language(_selectedlanguage)
    # If successful, go ahead!
    if isLanguageAvailable:
        # Calling function to get the repository count
        repositoryData = getRepositoryCount(str(_selectedlanguage))
        # Creating dictionary to store the data
        urlCount = collections.OrderedDict()
        # Iterating through the available data
        for i in repositoryData:
            # Storing data in the dictionary
            urlCount[i.year] = i.count
        # Sorted the dictionary
        stats = collections.OrderedDict(sorted(urlCount.items()))
        # Converting current_year to list of string for rendering
        # in the template
        current_year = map(str, (list(stats.keys())))
        # Converting current_count to list of integer for projecting
        # the future count. PLEASE NOTE: this could be avoided but
        # converting as a precautionary measures as data once received
        # from the api was in string
        current_count = map(int, list(stats.values()))
        # Storing prediction data for rendering in the template
        pred_year, pred_count = getProjectionRepositoryCount(current_count)
        # Storing performance etrics for rendering in the template
        estimate_error, goodness_fit, standard_deviation_error = getIndicativeMetrics(pred_year, pred_count)
        # Converting pred_year to list of string for rendering in the template
        pred_year = map(str, (list(pred_year)))
        # Returning the object
        return render_template('template.html', **locals())
    else:
        # Logging the error
        app.logger.error('Something went wrong!')
        # Returning the object
        return not_found()


@app.route("/")
def initialResponse():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welome to the Flask API for Github Repository Prediction'
    }
    js = json.dumps(message)
    # Specifing the response type
    resp = Response(js, mimetype='application/json')
    # Returning the object
    return resp


if __name__ == "__main__":
    # Running app in debug mode
    app.run(debug=True)
