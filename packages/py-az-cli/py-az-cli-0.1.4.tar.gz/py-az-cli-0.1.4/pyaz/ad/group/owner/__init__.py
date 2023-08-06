from .... pyaz_utils import _call_az

def list(group):
    '''
    List group owners.
    '''
    return _call_az("az ad group owner list", locals())


def add(group, owner_object_id):
    '''
    Add a group owner.
    '''
    return _call_az("az ad group owner add", locals())


def remove(group, owner_object_id):
    '''
    Remove a group owner.
    '''
    return _call_az("az ad group owner remove", locals())

