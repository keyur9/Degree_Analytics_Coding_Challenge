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
    original_years = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    original_count = np.array(count)
    curve_fit = np.polyfit(original_years, original_count, 3)
    poly_fit = np.poly1d(curve_fit)
    predicted_years = np.append(original_years, [11, 12, 13, 14, 15])
    predicted_years = predicted_years + 2008
    original_years = original_years + 2008
    predicted_count = []
    for i in range(0, 15):
        predicted_count.append(poly_fit(i+1))
    return predicted_years, predicted_count


def getRepositoryCount(language):
    """Function calling Github API to get the number of repository by year."""
    urlCount = collections.OrderedDict()
    start_date = datetime.date(2008, 01, 01)
    end_date = datetime.date(2018, 01, 01)
    while start_date < end_date:
        start_date = start_date + relativedelta(years=1)
        url = 'https://api.github.com/search/repositories?q=language:' + language + '+created:<' + start_date.strftime('%Y')
        r = requests.get(url)
        response_dict = r.json()
        urlCount[parser.parse(start_date.strftime('%Y')).year] = response_dict['total_count']
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
