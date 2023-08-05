from .... pyaz_utils import call_az

def merge(file, name, vault_name, certificate_attributes=None, disabled=None, expires=None, not_before=None, tags=None):
    return call_az("az keyvault certificate pending merge", locals())


def show(name, vault_name):
    return call_az("az keyvault certificate pending show", locals())


def delete(name, vault_name):
    return call_az("az keyvault certificate pending delete", locals())

