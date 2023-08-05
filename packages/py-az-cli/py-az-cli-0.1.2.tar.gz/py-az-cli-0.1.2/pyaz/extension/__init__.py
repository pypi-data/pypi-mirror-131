from .. pyaz_utils import call_az

def add(index=None, name=None, pip_extra_index_urls=None, pip_proxy=None, source=None, system=None, upgrade=None, version=None, yes=None):
    '''
    Add an extension.
    '''
    return call_az("az extension add", locals())


def remove(name):
    '''
    Remove an extension.
    '''
    return call_az("az extension remove", locals())


def list():
    '''
    List the installed extensions.
    '''
    return call_az("az extension list", locals())


def show(name):
    '''
    Show an extension.
    '''
    return call_az("az extension show", locals())


def list_available(index=None, show_details=None):
    '''
    List publicly available extensions.
    '''
    return call_az("az extension list-available", locals())


def update(name, index=None, pip_extra_index_urls=None, pip_proxy=None):
    '''
    Update an extension.
    '''
    return call_az("az extension update", locals())


def list_versions(name, index=None):
    '''
    List available versions for an extension.
    '''
    return call_az("az extension list-versions", locals())

