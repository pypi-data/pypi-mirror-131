from ... pyaz_utils import call_az

def create(location, resource_group, service_name, service_topology_name, target_location, target_subscription_id, tags=None):
    '''
    Creates a service under the specified service topology.
    '''
    return call_az("az deploymentmanager service create", locals())


def delete(resource_group, service_name, service_topology_name):
    '''
    Deletes the service topology.
    '''
    return call_az("az deploymentmanager service delete", locals())


def show(resource_group, service_name, service_topology_name):
    '''
    Get the details of a service.
    '''
    return call_az("az deploymentmanager service show", locals())


def list(resource_group, service_topology_name):
    '''
    List all services in a service topology.
    '''
    return call_az("az deploymentmanager service list", locals())


def update(resource_group, service_name, service_topology_name, add=None, force_string=None, remove=None, set=None, tags=None, target_location=None, target_subscription_id=None):
    '''
    Updates the service.
    '''
    return call_az("az deploymentmanager service update", locals())

