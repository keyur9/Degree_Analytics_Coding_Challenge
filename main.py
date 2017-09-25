# -*- coding: utf-8 -*-

"""
Created on Fri Sep 22 12:38:56 2017.
@author: keyur
 Python Flask API that shows a chart and data projection
 for the amount of Python and R Repos that will be created
 over the next 5 years on Github (use the github api for retrieving data)
"""

from routes import app

if __name__ == "__main__":
    # Running app in debug mode
    app.run(debug=True)
