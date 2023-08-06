from .... pyaz_utils import _call_az

def list(database_rid, instance_id, location, end_time=None, start_time=None):
    '''
    List all the versions of all the sql containers that were created / modified / deleted in the given database and restorable account.
    '''
    return _call_az("az cosmosdb sql restorable-container list", locals())

