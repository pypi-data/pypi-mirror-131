from ... pyaz_utils import call_az
from . import package, summary


def list(name, resource_group, maxresults=None):
    return call_az("az batch application list", locals())


def show(application_name, name, resource_group):
    return call_az("az batch application show", locals())


def create(application_name, name, resource_group, parameters=None):
    return call_az("az batch application create", locals())


def set(application_name, name, resource_group, allow_updates=None, default_version=None, display_name=None):
    '''
    Update properties for a Batch application.
    '''
    return call_az("az batch application set", locals())


def delete(application_name, name, resource_group, yes=None):
    return call_az("az batch application delete", locals())

