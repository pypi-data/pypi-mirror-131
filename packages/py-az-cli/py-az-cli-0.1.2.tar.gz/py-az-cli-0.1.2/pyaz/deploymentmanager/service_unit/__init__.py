from ... pyaz_utils import call_az

def create(deployment_mode, parameters_path, resource_group, service_name, service_topology_name, service_unit_name, target_resource_group, template_path, location=None, tags=None):
    '''
    Creates a service unit under the specified service and service topology.
    '''
    return call_az("az deploymentmanager service-unit create", locals())


def delete(resource_group, service_name, service_topology_name, service_unit_name):
    '''
    Deletes the service unit.
    '''
    return call_az("az deploymentmanager service-unit delete", locals())


def show(resource_group, service_name, service_topology_name, service_unit_name):
    '''
    Get the details of a service unit.
    '''
    return call_az("az deploymentmanager service-unit show", locals())


def list(resource_group, service_name, service_topology_name):
    '''
    List all service units in a service.
    '''
    return call_az("az deploymentmanager service-unit list", locals())


def update(resource_group, service_name, service_topology_name, service_unit_name, add=None, deployment_mode=None, force_string=None, parameters_path=None, remove=None, set=None, tags=None, target_resource_group=None, template_path=None):
    '''
    Updates the service unit.
    '''
    return call_az("az deploymentmanager service-unit update", locals())

