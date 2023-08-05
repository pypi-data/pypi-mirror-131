from ... pyaz_utils import call_az
from . import alert


def list(resource, aggregation=None, dimension=None, end_time=None, filter=None, interval=None, metadata=None, metrics=None, namespace=None, offset=None, orderby=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None, start_time=None, top=None):
    '''
    List the metric values for a resource.
    '''
    return call_az("az monitor metrics list", locals())


def list_definitions(resource, namespace=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None):
    '''
    List the metric definitions for the resource.
    '''
    return call_az("az monitor metrics list-definitions", locals())


def list_namespaces(resource_uri, start_time=None):
    '''
    List the metric namespaces for the resource.
    '''
    return call_az("az monitor metrics list-namespaces", locals())

