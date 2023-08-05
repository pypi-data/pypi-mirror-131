from .... pyaz_utils import call_az

def list(dps_name, resource_group):
    '''
    List all shared access policies in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps access-policy list", locals())


def show(access_policy_name, dps_name, resource_group):
    '''
    Show details of a shared access policies in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps access-policy show", locals())


def create(access_policy_name, dps_name, resource_group, rights, no_wait=None, primary_key=None, secondary_key=None):
    '''
    Create a new shared access policy in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps access-policy create", locals())


def update(access_policy_name, dps_name, resource_group, no_wait=None, primary_key=None, rights=None, secondary_key=None):
    '''
    Update a shared access policy in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps access-policy update", locals())


def delete(access_policy_name, dps_name, resource_group, no_wait=None):
    '''
    Delete a shared access policies in an Azure IoT Hub device provisioning service.
    '''
    return call_az("az iot dps access-policy delete", locals())

