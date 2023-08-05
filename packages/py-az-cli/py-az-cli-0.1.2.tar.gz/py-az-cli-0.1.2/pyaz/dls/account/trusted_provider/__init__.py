from .... pyaz_utils import call_az

def create(account, id_provider, trusted_id_provider_name, resource_group=None):
    return call_az("az dls account trusted-provider create", locals())


def update(account, trusted_id_provider_name, id_provider=None, resource_group=None):
    return call_az("az dls account trusted-provider update", locals())


def list(account, resource_group=None):
    return call_az("az dls account trusted-provider list", locals())


def show(account, trusted_id_provider_name, resource_group=None):
    return call_az("az dls account trusted-provider show", locals())


def delete(account, trusted_id_provider_name, resource_group=None):
    return call_az("az dls account trusted-provider delete", locals())

