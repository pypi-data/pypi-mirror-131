from ... pyaz_utils import call_az

def create(location, resource_group, service_topology_name, artifact_source=None, tags=None):
    '''
    Creates a service topology.
    '''
    return call_az("az deploymentmanager service-topology create", locals())


def delete(resource_group, service_topology_name):
    '''
    Deletes the service topology.
    '''
    return call_az("az deploymentmanager service-topology delete", locals())


def show(resource_group, service_topology_name):
    '''
    Get the details of a service topology.
    '''
    return call_az("az deploymentmanager service-topology show", locals())


def list(resource_group):
    '''
    List all service topologies in a resource group.
    '''
    return call_az("az deploymentmanager service-topology list", locals())


def update(resource_group, service_topology_name, add=None, artifact_source=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Updates the service topology.
    '''
    return call_az("az deploymentmanager service-topology update", locals())

