"""This module will get the projection count of the repository."""

import numpy as np
import imp
# Importing global module
globalVariable = imp.load_source('*', './app/global.py')


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
    start_year = globalVariable.startYear
    # Current data of repositories count for the language
    original_count = np.array(count)
    # Current data of years of repositories created
    original_years = np.array(range(1, len(original_count) + 1))
    # polyfit : Least squares polynomial fit.
    # Fitting the polynomial with 3rd degree
    curve_fit = np.polyfit(original_years, original_count, globalVariable.polyfitDegree)
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
