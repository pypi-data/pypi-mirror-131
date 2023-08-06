from .... pyaz_utils import _call_az

def show(name, resource_group=None):
    '''
    Get IoT Hub's device streams endpoints.
    '''
    return _call_az("az iot hub devicestream show", locals())

