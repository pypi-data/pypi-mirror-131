from ..... pyaz_utils import call_az

def show(account_name, name, resource_group):
    '''
    Get the throughput of the Cassandra keyspace under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb cassandra keyspace throughput show", locals())


def update(account_name, name, resource_group, max_throughput=None, throughput=None):
    '''
    Update the throughput of the Cassandra keyspace under an Azure Cosmos DB account.
    '''
    return call_az("az cosmosdb cassandra keyspace throughput update", locals())


def migrate(account_name, name, resource_group, throughput_type):
    '''
    Migrate the throughput of the Cassandra keyspace between autoscale and manually provisioned.
    '''
    return call_az("az cosmosdb cassandra keyspace throughput migrate", locals())

