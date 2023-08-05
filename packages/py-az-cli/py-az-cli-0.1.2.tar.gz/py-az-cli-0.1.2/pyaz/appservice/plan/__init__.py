from ... pyaz_utils import call_az

def create(name, resource_group, app_service_environment=None, hyper_v=None, is_linux=None, location=None, no_wait=None, number_of_workers=None, per_site_scaling=None, sku=None, tags=None, zone_redundant=None):
    '''
    Create an app service plan.
    '''
    return call_az("az appservice plan create", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete an app service plan.
    '''
    return call_az("az appservice plan delete", locals())


def list(resource_group=None):
    '''
    List app service plans.
    '''
    return call_az("az appservice plan list", locals())


def show(name, resource_group):
    '''
    Get the app service plans for a resource group or a set of resource groups.
    '''
    return call_az("az appservice plan show", locals())


def update(name, resource_group, add=None, force_string=None, no_wait=None, number_of_workers=None, remove=None, set=None, sku=None):
    '''
    Update an app service plan.
    '''
    return call_az("az appservice plan update", locals())

