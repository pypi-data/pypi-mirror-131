from .... pyaz_utils import call_az

def create(endpoints, key, name, value, resource_group=None):
    '''
    Create a message enrichment for chosen endpoints in your IoT Hub
    '''
    return call_az("az iot hub message-enrichment create", locals())


def list(name, resource_group=None):
    '''
    Get information on all message enrichments for your IoT Hub
    '''
    return call_az("az iot hub message-enrichment list", locals())


def delete(key, name, resource_group=None):
    '''
    Delete a message enrichment in your IoT hub (by key)
    '''
    return call_az("az iot hub message-enrichment delete", locals())


def update(endpoints, key, name, value, resource_group=None):
    '''
    Update a message enrichment in your IoT hub (by key)
    '''
    return call_az("az iot hub message-enrichment update", locals())

