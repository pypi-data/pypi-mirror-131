from ... pyaz_utils import call_az
from . import backup_properties, encryption, identity


def create(location, name, resource_group, tags=None):
    '''
    Create a new Recovery Services vault.
    '''
    return call_az("az backup vault create", locals())


def show(name, resource_group):
    '''
    Show details of a particular Recovery service vault.
    '''
    return call_az("az backup vault show", locals())


def list(resource_group=None):
    '''
    List Recovery service vaults within a subscription.
    '''
    return call_az("az backup vault list", locals())


def delete(name, resource_group, force=None, yes=None):
    '''
    Delete an existing Recovery services vault.
    '''
    return call_az("az backup vault delete", locals())

