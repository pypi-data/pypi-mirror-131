from ... pyaz_utils import _call_az

def create(categories, days, enabled, location, locations, name, service_bus_rule_id=None, storage_account_id=None, tags=None):
    '''
    Create a log profile.
    '''
    return _call_az("az monitor log-profiles create", locals())


def delete(name):
    return _call_az("az monitor log-profiles delete", locals())


def show(name):
    return _call_az("az monitor log-profiles show", locals())


def list():
    return _call_az("az monitor log-profiles list", locals())


def update(name, add=None, force_string=None, remove=None, set=None):
    '''
    Update a log profile.
    '''
    return _call_az("az monitor log-profiles update", locals())

