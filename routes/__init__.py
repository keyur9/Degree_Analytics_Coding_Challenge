from flask import Flask
import logging
import imp

globalVariable = imp.load_source('*', './app/global.py')
# Place where app is defined
app = Flask(__name__, template_folder=globalVariable.tmplDir)

"""Creating app.log file for logging purpose."""
app.logger.addHandler(logging.FileHandler(globalVariable.logFileName))
app.logger.setLevel(logging.INFO)

import routes.routeEndpoints
