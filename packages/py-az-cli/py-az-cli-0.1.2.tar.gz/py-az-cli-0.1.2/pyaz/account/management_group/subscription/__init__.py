from .... pyaz_utils import call_az

def add(name, subscription):
    '''
    Add a subscription to a management group.
    '''
    return call_az("az account management-group subscription add", locals())


def remove(name, subscription):
    '''
    Remove an existing subscription from a management group.
    '''
    return call_az("az account management-group subscription remove", locals())

