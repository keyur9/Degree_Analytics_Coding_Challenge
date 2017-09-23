# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:38:56 2017

@author: keyur
"""
# In[]

"""
# Import Modules
"""
from flask import Flask, render_template, Response, jsonify
import collections
import os
import json
import requests
import dateutil.parser as parser
import logging
import datetime
from dateutil.relativedelta import relativedelta
 
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
 
# In[]

"""
# Logging
"""
file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# In[]

def getRepositoryCount(language):
    """
    # Function calling Github API to get the number of repository by year
    """
    urlCount = collections.OrderedDict()
    start_date = datetime.date(2008, 01, 01)
    end_date = datetime.date(2018, 01, 01)
    while start_date < end_date:
        start_date = start_date + relativedelta(years=1)    
        url='https://api.github.com/search/repositories?q=language:' + language + '+created:<' + start_date.strftime('%Y')
        r = requests.get(url)
        response_dict = r.json()
        urlCount[parser.parse(start_date.strftime('%Y')).year] =  response_dict['total_count']
    return urlCount
 
# In[]
@app.errorhandler(404)
def not_found(error=None):
    """
    # Error handling
    """
    message = {
            'status': 404,
            'message': 'Something went wrong: ' ,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
# In[]
    
@app.route("/api/v1.0/charts/<language>", methods = ['GET'])
def index(language):
    """
    # Function rendering charts
    """
    availableLanguage = ['Python','R']
    if language in availableLanguage:
        _selectedlanguage = language
        stats = collections.OrderedDict(sorted(getRepositoryCount(str(_selectedlanguage)).items()))
        year = map(str,(list(stats.keys())))
        count = map(int,list(stats.values()))
        return render_template('template.html',**locals()) 
    else:
        app.logger.error('Something went wrong!')
        return not_found()
 
# In[]
@app.route("/")
def hello():
    """
    # Welcome API 
    """
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welome to the API'
    }
    js = json.dumps(message)

    resp = Response(js, mimetype='application/json')
    return resp


# In[] 
if __name__ == "__main__":
    app.run(debug=True)