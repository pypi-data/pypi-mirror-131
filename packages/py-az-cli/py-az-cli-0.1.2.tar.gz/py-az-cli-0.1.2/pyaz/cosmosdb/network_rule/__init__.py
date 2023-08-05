from ... pyaz_utils import call_az

def list(name, resource_group):
    return call_az("az cosmosdb network-rule list", locals())


def add(name, resource_group, subnet, ignore_missing_endpoint=None, vnet_name=None):
    return call_az("az cosmosdb network-rule add", locals())


def remove(name, resource_group, subnet, vnet_name=None):
    return call_az("az cosmosdb network-rule remove", locals())

