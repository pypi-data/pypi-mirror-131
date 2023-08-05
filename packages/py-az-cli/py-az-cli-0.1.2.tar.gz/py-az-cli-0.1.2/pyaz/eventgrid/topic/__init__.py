from ... pyaz_utils import call_az
from . import key


def show(name, resource_group):
    '''
    Get the details of a topic.
    '''
    return call_az("az eventgrid topic show", locals())


def delete(name, resource_group):
    '''
    Delete a topic.
    '''
    return call_az("az eventgrid topic delete", locals())


def list(odata_query=None, resource_group=None):
    '''
    List available topics.
    '''
    return call_az("az eventgrid topic list", locals())


def create(name, resource_group, extended_location_name=None, extended_location_type=None, identity=None, inbound_ip_rules=None, input_mapping_default_values=None, input_mapping_fields=None, input_schema=None, kind=None, location=None, public_network_access=None, sku=None, tags=None):
    '''
    Create a topic.
    '''
    return call_az("az eventgrid topic create", locals())


def update(name, resource_group, identity=None, inbound_ip_rules=None, public_network_access=None, sku=None, tags=None):
    '''
    Update a topic.
    '''
    return call_az("az eventgrid topic update", locals())

