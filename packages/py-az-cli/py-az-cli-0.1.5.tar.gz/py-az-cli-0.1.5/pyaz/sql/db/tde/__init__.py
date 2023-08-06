from .... pyaz_utils import _call_az

def set(database, resource_group, server, status):
    '''
    Sets a database's transparent data encryption configuration.
    '''
    return _call_az("az sql db tde set", locals())


def show(database, resource_group, server):
    return _call_az("az sql db tde show", locals())


def list_activity(database, resource_group, server):
    return _call_az("az sql db tde list-activity", locals())

