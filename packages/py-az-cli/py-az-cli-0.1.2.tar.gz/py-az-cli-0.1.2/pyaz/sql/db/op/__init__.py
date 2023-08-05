from .... pyaz_utils import call_az

def list(database, resource_group, server):
    return call_az("az sql db op list", locals())


def cancel(database, name, resource_group, server):
    return call_az("az sql db op cancel", locals())

