from ... pyaz_utils import call_az
from . import access_policy, certificate, linked_hub


def list(resource_group=None):
    '''
    List Azure IoT Hub device provisioning services.
    '''
    return call_az("az iot dps list", locals())


def show(name, resource_group=None):
    '''
    Get the details of an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps show", locals())


def create(name, resource_group, location=None, sku=None, tags=None, unit=None):
    '''
    Create an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps create", locals())


def delete(name, resource_group):
    '''
    Delete an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps delete", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None):
    '''
    Update an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps update", locals())

