from .... pyaz_utils import call_az

def create(endpoint_name, endpoint_resource_group, endpoint_subscription_id, endpoint_type, hub_name, auth_type=None, batch_frequency=None, chunk_size=None, connection_string=None, container_name=None, encoding=None, endpoint_uri=None, entity_path=None, file_name_format=None, identity=None, resource_group=None):
    '''
    Add an endpoint to your IoT Hub.
    '''
    return call_az("az iot hub routing-endpoint create", locals())


def show(endpoint_name, hub_name, resource_group=None):
    '''
    Get information on mentioned endpoint for your IoT Hub.
    '''
    return call_az("az iot hub routing-endpoint show", locals())


def list(hub_name, endpoint_type=None, resource_group=None):
    '''
    Get information on all the endpoints for your IoT Hub.
    '''
    return call_az("az iot hub routing-endpoint list", locals())


def delete(hub_name, endpoint_name=None, endpoint_type=None, resource_group=None):
    '''
    Delete all or mentioned endpoint for your IoT Hub.
    '''
    return call_az("az iot hub routing-endpoint delete", locals())

