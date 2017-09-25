"""This module will send message to user."""

from flask import jsonify
import imp
# Importing global module
globalVariable = imp.load_source('*', './app/global.py')


def no_data_found(error_description):
    """Send message to user with Ok status."""
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
    resp.status_code = globalVariable.okStatusCode
    # Returning the object
    return resp
