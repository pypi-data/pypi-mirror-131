from .... pyaz_utils import _call_az

def postgres(client_type=None, connection=None, database=None, name=None, new=None, no_wait=None, resource_group=None, secret=None, server=None, source_id=None, target_id=None, target_resource_group=None):
    '''
    Create a webapp connection to postgres.
    '''
    return _call_az("az webapp connection create postgres", locals())


def postgres_flexible(client_type=None, connection=None, database=None, name=None, no_wait=None, resource_group=None, secret=None, server=None, source_id=None, target_id=None, target_resource_group=None):
    '''
    Create a webapp connection to postgres-flexible.
    '''
    return _call_az("az webapp connection create postgres-flexible", locals())


def mysql(client_type=None, connection=None, database=None, name=None, no_wait=None, resource_group=None, secret=None, server=None, source_id=None, target_id=None, target_resource_group=None):
    '''
    Create a webapp connection to mysql.
    '''
    return _call_az("az webapp connection create mysql", locals())


def mysql_flexible(client_type=None, connection=None, database=None, name=None, no_wait=None, resource_group=None, secret=None, server=None, source_id=None, target_id=None, target_resource_group=None):
    '''
    Create a webapp connection to mysql-flexible.
    '''
    return _call_az("az webapp connection create mysql-flexible", locals())


def cosmos_cassandra(account=None, client_type=None, connection=None, key_space=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to cosmos-cassandra.
    '''
    return _call_az("az webapp connection create cosmos-cassandra", locals())


def cosmos_gremlin(account=None, client_type=None, connection=None, database=None, graph=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to cosmos-gremlin.
    '''
    return _call_az("az webapp connection create cosmos-gremlin", locals())


def cosmos_mongo(account=None, client_type=None, connection=None, database=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to cosmos-mongo.
    '''
    return _call_az("az webapp connection create cosmos-mongo", locals())


def cosmos_table(account=None, client_type=None, connection=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, table=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to cosmos-table.
    '''
    return _call_az("az webapp connection create cosmos-table", locals())


def cosmos_sql(account=None, client_type=None, connection=None, database=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to cosmos-sql.
    '''
    return _call_az("az webapp connection create cosmos-sql", locals())


def storage_blob(account=None, client_type=None, connection=None, name=None, new=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to storage-blob.
    '''
    return _call_az("az webapp connection create storage-blob", locals())


def storage_queue(account=None, client_type=None, connection=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to storage-queue.
    '''
    return _call_az("az webapp connection create storage-queue", locals())


def storage_file(account=None, client_type=None, connection=None, name=None, no_wait=None, resource_group=None, secret=None, source_id=None, target_id=None, target_resource_group=None):
    '''
    Create a webapp connection to storage-file.
    '''
    return _call_az("az webapp connection create storage-file", locals())


def storage_table(account=None, client_type=None, connection=None, name=None, no_wait=None, resource_group=None, secret=None, source_id=None, target_id=None, target_resource_group=None):
    '''
    Create a webapp connection to storage-table.
    '''
    return _call_az("az webapp connection create storage-table", locals())


def keyvault(client_type=None, connection=None, name=None, new=None, no_wait=None, resource_group=None, service_principal=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None, vault=None):
    '''
    Create a webapp connection to keyvault.
    '''
    return _call_az("az webapp connection create keyvault", locals())


def signalr(client_type=None, connection=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, signalr=None, source_id=None, system_identity=None, target_id=None, target_resource_group=None, user_identity=None):
    '''
    Create a webapp connection to signalr.
    '''
    return _call_az("az webapp connection create signalr", locals())


def confluent_cloud(bootstrap_server, kafka_key, kafka_secret, schema_key, schema_registry, schema_secret, client_type=None, connection=None, name=None, no_wait=None, resource_group=None, source_id=None):
    '''
    Create a webapp connection to confluent-cloud.
    '''
    return _call_az("az webapp connection create confluent-cloud", locals())

