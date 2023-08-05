from .... pyaz_utils import call_az

def list(elastic_pool, resource_group, server):
    return call_az("az sql elastic-pool op list", locals())


def cancel(elastic_pool, name, resource_group, server):
    return call_az("az sql elastic-pool op cancel", locals())

