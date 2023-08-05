from .... pyaz_utils import call_az

def postgres(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None):
    '''
    Update a webapp to postgres connection.
    '''
    return call_az("az webapp connection update postgres", locals())


def postgres_flexible(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None):
    '''
    Update a webapp to postgres-flexible connection.
    '''
    return call_az("az webapp connection update postgres-flexible", locals())


def mysql(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None):
    '''
    Update a webapp to mysql connection.
    '''
    return call_az("az webapp connection update mysql", locals())


def mysql_flexible(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None):
    '''
    Update a webapp to mysql-flexible connection.
    '''
    return call_az("az webapp connection update mysql-flexible", locals())


def cosmos_cassandra(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to cosmos-cassandra connection.
    '''
    return call_az("az webapp connection update cosmos-cassandra", locals())


def cosmos_gremlin(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to cosmos-gremlin connection.
    '''
    return call_az("az webapp connection update cosmos-gremlin", locals())


def cosmos_mongo(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to cosmos-mongo connection.
    '''
    return call_az("az webapp connection update cosmos-mongo", locals())


def cosmos_table(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to cosmos-table connection.
    '''
    return call_az("az webapp connection update cosmos-table", locals())


def cosmos_sql(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to cosmos-sql connection.
    '''
    return call_az("az webapp connection update cosmos-sql", locals())


def storage_blob(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to storage-blob connection.
    '''
    return call_az("az webapp connection update storage-blob", locals())


def storage_queue(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to storage-queue connection.
    '''
    return call_az("az webapp connection update storage-queue", locals())


def storage_file(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None):
    '''
    Update a webapp to storage-file connection.
    '''
    return call_az("az webapp connection update storage-file", locals())


def storage_table(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None):
    '''
    Update a webapp to storage-table connection.
    '''
    return call_az("az webapp connection update storage-table", locals())


def keyvault(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to keyvault connection.
    '''
    return call_az("az webapp connection update keyvault", locals())


def signalr(client_type=None, connection=None, id=None, name=None, no_wait=None, resource_group=None, secret=None, service_principal=None, system_identity=None, user_identity=None):
    '''
    Update a webapp to signalr connection.
    '''
    return call_az("az webapp connection update signalr", locals())


def confluent_cloud(connection, bootstrap_server=None, client_type=None, kafka_key=None, kafka_secret=None, name=None, no_wait=None, resource_group=None, schema_key=None, schema_registry=None, schema_secret=None, source_id=None):
    '''
    Update a webapp to confluent-cloud connection.
    '''
    return call_az("az webapp connection update confluent-cloud", locals())

