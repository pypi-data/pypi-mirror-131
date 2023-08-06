from .... pyaz_utils import _call_az

def create(application_name, name, package_file, resource_group, version_name):
    '''
    Create a Batch application package record and activate it.
    '''
    return _call_az("az batch application package create", locals())


def delete(application_name, name, resource_group, version_name, yes=None):
    return _call_az("az batch application package delete", locals())


def show(application_name, name, resource_group, version_name):
    return _call_az("az batch application package show", locals())


def activate(application_name, format, name, resource_group, version_name):
    '''
    Activates a Batch application package.
    '''
    return _call_az("az batch application package activate", locals())


def list(application_name, name, resource_group, maxresults=None):
    return _call_az("az batch application package list", locals())

