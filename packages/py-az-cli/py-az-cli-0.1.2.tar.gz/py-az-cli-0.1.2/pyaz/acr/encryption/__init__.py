from ... pyaz_utils import call_az

def show(name, resource_group=None):
    '''
    Show the container registry's encryption details
    '''
    return call_az("az acr encryption show", locals())


def rotate_key(name, identity=None, key_encryption_key=None, resource_group=None):
    '''
    Rotate (update) the container registry's encryption key
    '''
    return call_az("az acr encryption rotate-key", locals())

