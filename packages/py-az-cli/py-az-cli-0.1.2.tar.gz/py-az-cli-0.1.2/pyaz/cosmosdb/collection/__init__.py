from ... pyaz_utils import call_az

def show(collection_name, db_name, key=None, name=None, resource_group_name=None, url_connection=None):
    return call_az("az cosmosdb collection show", locals())


def list(db_name, key=None, name=None, resource_group_name=None, url_connection=None):
    return call_az("az cosmosdb collection list", locals())


def exists(collection_name, db_name, key=None, name=None, resource_group_name=None, url_connection=None):
    return call_az("az cosmosdb collection exists", locals())


def create(collection_name, db_name, default_ttl=None, indexing_policy=None, key=None, name=None, partition_key_path=None, resource_group_name=None, throughput=None, url_connection=None):
    return call_az("az cosmosdb collection create", locals())


def delete(collection_name, db_name, key=None, name=None, resource_group_name=None, url_connection=None, yes=None):
    return call_az("az cosmosdb collection delete", locals())


def update(collection_name, db_name, default_ttl=None, indexing_policy=None, key=None, name=None, resource_group_name=None, throughput=None, url_connection=None):
    return call_az("az cosmosdb collection update", locals())

