from .... pyaz_utils import call_az

def list(hub_name, resource_group=None):
    '''
    List shared access policies of an IoT hub.
    '''
    return call_az("az iot hub policy list", locals())


def show(hub_name, name, resource_group=None):
    '''
    Get the details of a shared access policy of an IoT hub.
    '''
    return call_az("az iot hub policy show", locals())


def create(hub_name, name, permissions, resource_group=None):
    '''
    Create a new shared access policy in an IoT hub.
    '''
    return call_az("az iot hub policy create", locals())


def delete(hub_name, name, resource_group=None):
    '''
    Delete a shared access policy from an IoT hub.
    '''
    return call_az("az iot hub policy delete", locals())


def renew_key(hub_name, name, renew_key, no_wait=None, resource_group=None):
    '''
    Regenerate keys of a shared access policy of an IoT hub.
    '''
    return call_az("az iot hub policy renew-key", locals())

