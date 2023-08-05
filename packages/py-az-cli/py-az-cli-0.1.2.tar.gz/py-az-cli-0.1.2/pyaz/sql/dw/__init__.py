from ... pyaz_utils import call_az

def create(name, resource_group, server, backup_storage_redundancy=None, collation=None, max_size=None, no_wait=None, service_objective=None, tags=None, zone_redundant=None):
    '''
    Create a data warehouse.
    '''
    return call_az("az sql dw create", locals())


def show(name, resource_group, server):
    '''
    Get the details for a data warehouse.
    '''
    return call_az("az sql dw show", locals())


def list(resource_group, server):
    '''
    List data warehouses for a server.
    '''
    return call_az("az sql dw list", locals())


def delete(name, resource_group, server, no_wait=None, yes=None):
    '''
    Delete a data warehouse.
    '''
    return call_az("az sql dw delete", locals())


def pause(name, resource_group, server):
    return call_az("az sql dw pause", locals())


def resume(name, resource_group, server):
    return call_az("az sql dw resume", locals())


def update(name, resource_group, server, add=None, force_string=None, max_size=None, no_wait=None, remove=None, service_objective=None, set=None):
    '''
    Update a data warehouse.
    '''
    return call_az("az sql dw update", locals())

