from .... pyaz_utils import call_az

def assign(name, resource_group=None, role=None, scopes=None, system_assigned=None, user_assigned=None):
    '''
    Assign managed identities to an IoT Hub
    '''
    return call_az("az iot hub identity assign", locals())


def show(name, resource_group=None):
    '''
    Show the identity properties of an IoT Hub
    '''
    return call_az("az iot hub identity show", locals())


def remove(name, resource_group=None, system_assigned=None, user_assigned=None):
    '''
    Remove managed identities from an IoT Hub
    '''
    return call_az("az iot hub identity remove", locals())

