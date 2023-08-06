from ... pyaz_utils import _call_az
from . import policy


def show(account_name, name, pool_name, resource_group, volume_name):
    '''
    Get the specified ANF snapshot.
    '''
    return _call_az("az netappfiles snapshot show", locals())


def list(account_name, pool_name, resource_group, volume_name):
    '''
    List the snapshots of an ANF volume.
    '''
    return _call_az("az netappfiles snapshot list", locals())


def delete(account_name, name, pool_name, resource_group, volume_name):
    '''
    Delete the specified ANF snapshot.
    '''
    return _call_az("az netappfiles snapshot delete", locals())


def create(account_name, location, name, pool_name, resource_group, volume_name):
    '''
    Create a new Azure NetApp Files (ANF) snapshot.
    '''
    return _call_az("az netappfiles snapshot create", locals())


def update(account_name, body, name, pool_name, resource_group, volume_name):
    return _call_az("az netappfiles snapshot update", locals())

