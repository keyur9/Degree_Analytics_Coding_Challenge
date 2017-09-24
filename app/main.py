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

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


"""Logging."""
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


def getProjectionRepositoryCount(count):
    """Projection of repositories for next 5 years."""
    prediction_for_next_n_years = 5
    start_year = 2008
    original_count = np.array(count)
    original_years = np.array(range(1, len(original_count) + 1))
    curve_fit = np.polyfit(original_years, original_count, 3)
    poly_fit = np.poly1d(curve_fit)
    predicted_years = np.append(original_years, list(range(max(original_years) + 1, max(original_years)+(prediction_for_next_n_years) + 1, 1)))
    predicted_years = predicted_years + start_year
    original_years = original_years + start_year
    predicted_count = []
    for i in range(0, len(predicted_years)):
        predicted_count.append(poly_fit(i + 1))
    return predicted_years, predicted_count


def getIndicativeMetrics(pred_years, pred_count):
    """Few indicative metrics."""
    years = np.array(pred_years)
    count = np.array(pred_count)

    # Modeling with Numpy
    p, cov = np.polyfit(years, count, 3, cov=True)  # parameters and covariance from of the fit
    count_model = np.polyval(p, years)  # model using the fit parameters; NOTE: parameters here are coefficients

    # Statistics
    n = count.size                              # number of observations
    m = p.size                                    # number of parameters
    DF = n - m                                    # degrees of freedom

    # Estimates of Error in Data/Model
    resid = count - count_model
    chi2 = np.sum((resid/count_model)**2)  # chi-squared; estimates error in data
    chi2_red = chi2/(DF)  # reduced chi-squared; measures goodness of fit
    s_err = np.sqrt(np.sum(resid**2)/(DF))  # standard deviation of the error
    return chi2, chi2_red, s_err


def getRepositoryCount(language):
    """Function calling Github API to get the number of repository by year."""
    urlCount = collections.OrderedDict()
    start_date = datetime.date(2008, 01, 01)
    end_date = start_date + relativedelta(years=10)
    while start_date < end_date:
        start_date = start_date + relativedelta(years=1)
        url = 'https://api.github.com/search/repositories?q=language:' + language + '+created:<' + start_date.strftime('%Y')
        try:
            r = requests.get(url)
            response_dict = r.json()
            # error if not total_count
            urlCount[parser.parse(start_date.strftime('%Y')).year] = response_dict['total_count']
        except KeyError:
            app.logger.error(response_dict['message'])
            pass
        except requests.exceptions.ConnectionError:
            app.logger.error("We are not connected to the Internet, \
                            Let's connect to the internet and try agian")
        except requests.exceptions.Timeout as err:
            app.logger.error(err)
    return urlCount


@app.errorhandler(200)
def not_found(error=None):
    """Error handling."""
    message = {
      "message": "Validation Failed",
      "errors": [
        {
          "message": "Current API support R and Python language search only."
        }
      ]
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.route("/api/v1.0/projection/<language>", methods=['GET'])
def index(language):
    """Function rendering charts."""
    availableLanguage = ['Python', 'R']
    if language in availableLanguage:
        _selectedlanguage = language
        stats = collections.OrderedDict(sorted(getRepositoryCount(str(_selectedlanguage)).items()))
        year = map(str, (list(stats.keys())))
        count = map(int, list(stats.values()))
        pred_year, pred_count = getProjectionRepositoryCount(count)
        estimate_error, goodness_fit, standard_deviation_error = getIndicativeMetrics(pred_year, pred_count)
        pred_year = map(str, (list(pred_year)))
        return render_template('template.html', **locals())
    else:
        app.logger.error('Something went wrong!')
        return not_found()


@app.route("/")
def initialResponse():
    """Welcome API."""
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welome to the Flask API for Github Repository Prediction'
    }
    js = json.dumps(message)
    resp = Response(js, mimetype='application/json')
    return resp


if __name__ == "__main__":
    app.run(debug=True)
