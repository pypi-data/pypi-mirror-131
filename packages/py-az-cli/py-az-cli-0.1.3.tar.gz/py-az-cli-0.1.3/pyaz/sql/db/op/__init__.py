from .... pyaz_utils import _call_az

def list(database, resource_group, server):
    return _call_az("az sql db op list", locals())


def cancel(database, name, resource_group, server):
    return _call_az("az sql db op cancel", locals())

