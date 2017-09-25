"""This module is to declare global objects."""

import datetime
import os

# Currently supported languages
availableLanguages = ['Python', 'R']
# Assumption that we're predicting for next 5 years
prediction_for_next_n_years = 5
# Based on quick check using Github API, no records were found before 2008
# for R and python repositories. So fetching data staring 2008.
startYear = 2008
# Message if requested for other languages
languageError = 'Current API support R and Python language search only.'
# Message when multiple requests are send in less than a minute
noDataFetchError = 'As per github API limitation, we can only to fetch limited data in 1 minute. Please try after 1 minute.'
# Sending OK status
statusCode = 200
responseKeyTotalCount = 'total_count'
responseKeyMessage = 'message'
# Based on start date fetching data till date which comes to 10 years
relativeDeltaEndDate = 10
# Fetching data year-wise
relativeDeltaYear = 1
# Base URL of github repositories API
baseURL = 'https://api.github.com/search/repositories?q=language:'
# Based on quick check using Github API, no records were found before 2008
# for R and python repositories. So fetching data staring 2008.
startDate = datetime.date(2008, 01, 01)
# Template Name
templateName = 'template.html'
# Fitting the polynomial with 3rd degree.
# Providing better results than 2nd degree.
polyfitDegree = 3
# Message if no connection available
networkConnectionError = "We are not connected to the Internet, Let's connect to the internet and try agian"
# Message if no response is received
raiseTypeErrorMessage = 'Logging the TypeError as receive None response'
# Message while handling no response
handleTypeErrorMessage = 'Logging the TypeError while handling None response'
# Filter by created date
queryFilter = '+created:<'
# tmpl Dir
tmplDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'templates')
