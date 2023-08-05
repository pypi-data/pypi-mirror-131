from .... pyaz_utils import call_az

def list(id):
    '''
    List application owners.
    '''
    return call_az("az ad app owner list", locals())


def add(id, owner_object_id):
    '''
    Add an application owner.
    '''
    return call_az("az ad app owner add", locals())


def remove(id, owner_object_id):
    '''
    Remove an application owner.
    '''
    return call_az("az ad app owner remove", locals())

