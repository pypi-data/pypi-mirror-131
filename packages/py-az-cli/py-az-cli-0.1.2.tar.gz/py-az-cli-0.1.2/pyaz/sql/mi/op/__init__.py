from .... pyaz_utils import call_az

def list(managed_instance, resource_group):
    return call_az("az sql mi op list", locals())


def show(managed_instance, name, resource_group):
    return call_az("az sql mi op show", locals())


def cancel(managed_instance, name, resource_group):
    return call_az("az sql mi op cancel", locals())

