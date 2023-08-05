from ... pyaz_utils import call_az
from . import keys


def show(function_name, name, resource_group):
    '''
    Get the details of a function.
    '''
    return call_az("az functionapp function show", locals())


def delete(function_name, name, resource_group):
    '''
    Delete a function.
    '''
    return call_az("az functionapp function delete", locals())

