from .. pyaz_utils import call_az
from . import custom_domain, edge_node, endpoint, origin, origin_group, profile


def name_exists(name):
    '''
    Check the availability of a resource name. This is needed for resources where name is globally unique, such as a CDN endpoint.
    '''
    return call_az("az cdn name-exists", locals())


def usage():
    return call_az("az cdn usage", locals())

