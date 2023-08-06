from ..... pyaz_utils import _call_az

def show(account_name, keyspace_name, name, resource_group):
    '''
    Get the throughput of the Cassandra table under an Azure Cosmos DB Cassandra keyspace.
    '''
    return _call_az("az cosmosdb cassandra table throughput show", locals())


def update(account_name, keyspace_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Update the throughput of the Cassandra table under an Azure Cosmos DB Cassandra keyspace.
    '''
    return _call_az("az cosmosdb cassandra table throughput update", locals())


def migrate(account_name, keyspace_name, name, resource_group, throughput_type):
    '''
    Migrate the throughput of the Cassandra table between autoscale and manually provisioned.
    '''
    return _call_az("az cosmosdb cassandra table throughput migrate", locals())

