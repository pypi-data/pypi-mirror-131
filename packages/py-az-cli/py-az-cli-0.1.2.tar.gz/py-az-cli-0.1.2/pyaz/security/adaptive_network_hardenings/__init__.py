from ... pyaz_utils import call_az

def show(adaptive_network_hardenings_resource_name, resource_group, resource_name, resource_namespace, resource_type):
    '''
    Gets a single Adaptive Network Hardening resource.
    '''
    return call_az("az security adaptive_network_hardenings show", locals())


def list(resource_group, resource_name, resource_namespace, resource_type):
    '''
    Gets a list of Adaptive Network Hardenings resources in scope of an extended resource.
    '''
    return call_az("az security adaptive_network_hardenings list", locals())

