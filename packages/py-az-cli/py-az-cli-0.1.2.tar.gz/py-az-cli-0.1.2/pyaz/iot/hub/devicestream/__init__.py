from .... pyaz_utils import call_az

def show(name, resource_group=None):
    '''
    Get IoT Hub's device streams endpoints.
    '''
    return call_az("az iot hub devicestream show", locals())

