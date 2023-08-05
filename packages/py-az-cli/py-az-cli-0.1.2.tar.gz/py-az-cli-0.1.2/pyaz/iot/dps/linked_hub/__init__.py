from .... pyaz_utils import call_az

def list(dps_name, resource_group):
    '''
    List all linked IoT hubs in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps linked-hub list", locals())


def show(dps_name, linked_hub, resource_group):
    '''
    Show details of a linked IoT hub in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps linked-hub show", locals())


def create(connection_string, dps_name, location, resource_group, allocation_weight=None, apply_allocation_policy=None, no_wait=None):
    '''
    Create a linked IoT hub in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps linked-hub create", locals())


def update(dps_name, linked_hub, resource_group, allocation_weight=None, apply_allocation_policy=None, no_wait=None):
    '''
    Update a linked IoT hub in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps linked-hub update", locals())


def delete(dps_name, linked_hub, resource_group, no_wait=None):
    '''
    Update a linked IoT hub in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps linked-hub delete", locals())

