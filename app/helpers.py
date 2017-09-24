"""This module is to compare if the reuqested search is currently supported."""
import imp
module = imp.load_source('*', './app/global.py')


def compare_language(language):
    """
    Function to compare language.

    Parameters:
    language - The language for which we want perform the prediction.
    """
    if language in module.availableLanguages:
        return True
    else:
        return False
