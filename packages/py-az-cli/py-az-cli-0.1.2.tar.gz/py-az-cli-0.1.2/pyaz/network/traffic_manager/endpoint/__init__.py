from .... pyaz_utils import call_az

def show(name, profile_name, resource_group, type):
    '''
    Get the details of a traffic manager endpoint.
    '''
    return call_az("az network traffic-manager endpoint show", locals())


def delete(name, profile_name, resource_group, type):
    '''
    Delete a traffic manager endpoint.
    '''
    return call_az("az network traffic-manager endpoint delete", locals())


def create(name, profile_name, resource_group, type, custom_headers=None, endpoint_location=None, endpoint_monitor_status=None, endpoint_status=None, geo_mapping=None, min_child_endpoints=None, priority=None, subnets=None, target=None, target_resource_id=None, weight=None):
    '''
    Create a traffic manager endpoint.
    '''
    return call_az("az network traffic-manager endpoint create", locals())


def list(profile_name, resource_group, type=None):
    '''
    List traffic manager endpoints.
    '''
    return call_az("az network traffic-manager endpoint list", locals())


def update(name, profile_name, resource_group, add=None, custom_headers=None, endpoint_location=None, endpoint_monitor_status=None, endpoint_status=None, force_string=None, geo_mapping=None, min_child_endpoints=None, priority=None, remove=None, set=None, subnets=None, target=None, target_resource_id=None, type=None, weight=None):
    '''
    Update a traffic manager endpoint.
    '''
    return call_az("az network traffic-manager endpoint update", locals())


def show_geographic_hierarchy():
    '''
    Get the default geographic hierarchy used by the geographic traffic routing method.
    '''
    return call_az("az network traffic-manager endpoint show-geographic-hierarchy", locals())

