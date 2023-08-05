from .... pyaz_utils import call_az

def create(endpoint_name, hub_name, route_name, source_type, condition=None, enabled=None, resource_group=None):
    '''
    Create a route in IoT Hub.
    '''
    return call_az("az iot hub route create", locals())


def show(hub_name, route_name, resource_group=None):
    '''
    Get information about the route in IoT Hub.
    '''
    return call_az("az iot hub route show", locals())


def list(hub_name, resource_group=None, source_type=None):
    '''
    Get all the routes in IoT Hub.
    '''
    return call_az("az iot hub route list", locals())


def delete(hub_name, resource_group=None, route_name=None, source_type=None):
    '''
    Delete all or mentioned route for your IoT Hub.
    '''
    return call_az("az iot hub route delete", locals())


def update(hub_name, route_name, condition=None, enabled=None, endpoint_name=None, resource_group=None, source_type=None):
    '''
    Update a route in IoT Hub.
    '''
    return call_az("az iot hub route update", locals())


def test(hub_name, app_properties=None, body=None, resource_group=None, route_name=None, source_type=None, system_properties=None):
    '''
    Test all routes or mentioned route in IoT Hub.
    '''
    return call_az("az iot hub route test", locals())

