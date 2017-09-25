"""This module will calculate the performance metrics."""

import numpy as np
import imp
# Importing global module
globalVariable = imp.load_source('*', './app/global.py')


def getIndicativeMetrics(pred_years, pred_count):
    """
    Few indicative metrics.

    Parameters:
    pred_years - List of predicted years
    pred_count - List of predicted repositories count

    Return:
    chi2 - Estimate of error in the model
    chi2_red - Measure of goodness of fit
    s_err - Standard deviation of the error
    """
    # Storing the received data of predicted years
    years = np.array(pred_years)
    # Storing the received data of predicted number of repositories
    count = np.array(pred_count)
    # Modeling with Numpy
    # parameters and covariance from of the fit
    p, cov = np.polyfit(years, count, globalVariable.polyfitDegree, cov=True)
    # model using the fit parameters; NOTE: parameters here are coefficients
    count_model = np.polyval(p, years)
    # Statistics
    # number of observations
    n = count.size
    # number of parameters
    m = p.size
    # degrees of freedom
    DF = n - m
    # Estimates of Error in Data/Model
    resid = count - count_model
    # chi-squared; estimates error in data
    chi2 = np.sum((resid/count_model)**2)
    # reduced chi-squared; measures goodness of fit
    chi2_red = chi2/(DF)
    # standard deviation of the error
    s_err = np.sqrt(np.sum(resid**2)/(DF))
    # Returning the object
    return chi2, chi2_red, s_err
