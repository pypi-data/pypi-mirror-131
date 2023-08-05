from ... pyaz_utils import call_az
from . import key, topic


def show(name, resource_group):
    '''
    Get the details of a domain.
    '''
    return call_az("az eventgrid domain show", locals())


def list(odata_query=None, resource_group=None):
    '''
    List available domains.
    '''
    return call_az("az eventgrid domain list", locals())


def create(name, resource_group, identity=None, inbound_ip_rules=None, input_mapping_default_values=None, input_mapping_fields=None, input_schema=None, location=None, public_network_access=None, sku=None, tags=None):
    '''
    Create a domain.
    '''
    return call_az("az eventgrid domain create", locals())


def delete(name, resource_group):
    '''
    Delete a domain.
    '''
    return call_az("az eventgrid domain delete", locals())


def update(name, resource_group, identity=None, inbound_ip_rules=None, public_network_access=None, sku=None, tags=None):
    '''
    Update a domain.
    '''
    return call_az("az eventgrid domain update", locals())

