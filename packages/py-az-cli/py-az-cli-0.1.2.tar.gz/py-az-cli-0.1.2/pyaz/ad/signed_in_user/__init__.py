from ... pyaz_utils import call_az

def show():
    return call_az("az ad signed-in-user show", locals())


def list_owned_objects(type=None):
    '''
    Get the list of directory objects that are owned by the user
    '''
    return call_az("az ad signed-in-user list-owned-objects", locals())

