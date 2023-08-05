from .... pyaz_utils import call_az

def list(database_rid, instance_id, location):
    '''
    List all the versions of all the mongodb collections that were created / modified / deleted in the given database and restorable account.
    '''
    return call_az("az cosmosdb mongodb restorable-collection list", locals())

