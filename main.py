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
import numpy as np
import imp
import packages
# Importing module
module = imp.load_source('*', './app/helpers.py')
globalVariable = imp.load_source('*', './app/global.py')

# Place where app is defined
app = Flask(__name__, template_folder=globalVariable.tmplDir)


"""Creating app.log file for logging purpose."""
app.logger.addHandler(logging.FileHandler('app.log'))
app.logger.setLevel(logging.INFO)


@app.errorhandler(globalVariable.statusCode)
def not_found(error_description):
    """Handling error in case of unexpected requests."""
    # Message to the user
    message = {
      "message": "Message from the API",
      "errors": [
        {
            "message": error_description
        }
      ]
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = globalVariable.statusCode
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
        # repositoryData = getRepositoryCount(str(_selectedlanguage))
        repositoryData = packages.getRepositoryCount(str(_selectedlanguage))
        if not repositoryData:
            app.logger.error(globalVariable.noDataFetchError)
            return not_found(globalVariable.noDataFetchError)
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
        pred_year, pred_count = packages.getProjectionRepositoryCount(current_count)
        # Storing performance etrics for rendering in the template
        estimate_error, goodness_fit, standard_deviation_error = packages.getIndicativeMetrics(pred_year, pred_count)
        # Converting pred_year to list of string for rendering in the template
        pred_year = map(str, (list(pred_year)))
        # Returning the object
        return render_template(globalVariable.templateName, **locals())
    else:
        # Logging the error
        app.logger.error(globalVariable.languageError)
        # Returning the object
        return not_found(globalVariable.languageError)


@app.route("/")
def getinitialResponse():
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
