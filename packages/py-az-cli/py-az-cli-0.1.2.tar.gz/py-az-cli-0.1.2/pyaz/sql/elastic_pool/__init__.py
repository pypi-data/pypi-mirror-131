from ... pyaz_utils import call_az
from . import op


def create(name, resource_group, server, capacity=None, db_dtu_max=None, db_dtu_min=None, family=None, license_type=None, maint_config_id=None, max_size=None, no_wait=None, tags=None, tier=None, zone_redundant=None):
    '''
    Create an elastic pool.
    '''
    return call_az("az sql elastic-pool create", locals())


def delete(name, resource_group, server, no_wait=None):
    return call_az("az sql elastic-pool delete", locals())


def show(name, resource_group, server):
    return call_az("az sql elastic-pool show", locals())


def list(resource_group, server, skip=None):
    return call_az("az sql elastic-pool list", locals())


def update(name, resource_group, server, add=None, capacity=None, db_dtu_max=None, db_dtu_min=None, family=None, force_string=None, maint_config_id=None, max_size=None, no_wait=None, remove=None, set=None, tier=None, zone_redundant=None):
    '''
    Update an elastic pool.
    '''
    return call_az("az sql elastic-pool update", locals())


def list_dbs(name, resource_group, server):
    return call_az("az sql elastic-pool list-dbs", locals())


def list_editions(location, available=None, dtu=None, show_details=None, tier=None, vcores=None):
    '''
    List elastic pool editions available for the active subscription.
    '''
    return call_az("az sql elastic-pool list-editions", locals())

