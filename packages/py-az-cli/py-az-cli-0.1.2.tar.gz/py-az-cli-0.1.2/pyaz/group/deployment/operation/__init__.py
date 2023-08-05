from .... pyaz_utils import call_az

def list(name, resource_group, top=None):
    return call_az("az group deployment operation list", locals())


def show(name, operation_ids, resource_group):
    return call_az("az group deployment operation show", locals())

