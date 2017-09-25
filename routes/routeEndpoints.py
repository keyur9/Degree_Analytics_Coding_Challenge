from routes import app
from flask import Flask, render_template, Response, jsonify
import collections
import json
import logging
import imp
import packages
# Importing module
globalVariable = imp.load_source('*', './app/global.py')
helperModule = imp.load_source('*', globalVariable.heplerFilePath)


@app.errorhandler(globalVariable.notFoundStatusCode)
def not_found(error_description=None):
    """Send message to user with notFound 404 status."""
    # Message to the user
    message = {
      "message": "Message from the API",
      "errors": [
        {
            "message": "This route is not currently supported. Please refer API documentation."
        }
      ]
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = globalVariable.notFoundStatusCode
    # Returning the object
    return resp


@app.route("/api/v1.0/projection/<language>", methods=[globalVariable.routeMethods])
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
    isLanguageAvailable = helperModule.compare_language(_selectedlanguage)
    # If successful, go ahead!
    if isLanguageAvailable:
        # Calling function to get the repository count
        # repositoryData = getRepositoryCount(str(_selectedlanguage))
        repositoryData = packages.getRepositoryCount(str(_selectedlanguage))
        if not repositoryData:
            app.logger.error(globalVariable.noDataFetchError)
            return packages.no_data_found(globalVariable.noDataFetchError)
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
        return packages.no_data_found(globalVariable.languageError)


@app.route("/")
def getInitialResponse():
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
