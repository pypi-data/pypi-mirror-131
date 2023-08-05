from ... pyaz_utils import call_az

def create(name, resource_group, sku, is_linux=None, location=None, max_burst=None, number_of_workers=None, tags=None, zone_redundant=None):
    '''
    Create an App Service Plan for an Azure Function.
    '''
    return call_az("az functionapp plan create", locals())


def update(name, resource_group, add=None, force_string=None, max_burst=None, number_of_workers=None, remove=None, set=None, sku=None):
    '''
    Update an App Service plan for an Azure Function.
    '''
    return call_az("az functionapp plan update", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete an App Service Plan.
    '''
    return call_az("az functionapp plan delete", locals())


def list(resource_group=None):
    '''
    List App Service Plans.
    '''
    return call_az("az functionapp plan list", locals())


def show(name, resource_group):
    '''
    Get the App Service Plans for a resource group or a set of resource groups.
    '''
    return call_az("az functionapp plan show", locals())

