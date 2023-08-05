from .... pyaz_utils import call_az

def add(filter_name, auth_mode=None, connection_string=None, endpoint=None, feature=None, filter_parameters=None, index=None, key=None, label=None, name=None, yes=None):
    '''
    Add a filter to a feature flag.
    '''
    return call_az("az appconfig feature filter add", locals())


def delete(all=None, auth_mode=None, connection_string=None, endpoint=None, feature=None, filter_name=None, index=None, key=None, label=None, name=None, yes=None):
    '''
    Delete a filter from a feature flag.
    '''
    return call_az("az appconfig feature filter delete", locals())


def show(filter_name, auth_mode=None, connection_string=None, endpoint=None, feature=None, index=None, key=None, label=None, name=None):
    '''
    Show filters of a feature flag.
    '''
    return call_az("az appconfig feature filter show", locals())


def list(all=None, auth_mode=None, connection_string=None, endpoint=None, feature=None, key=None, label=None, name=None, top=None):
    '''
    List all filters for a feature flag.
    '''
    return call_az("az appconfig feature filter list", locals())

