from .... pyaz_utils import _call_az

def list(vault_name):
    return _call_az("az keyvault certificate contact list", locals())


def add(email, vault_name, name=None, phone=None):
    return _call_az("az keyvault certificate contact add", locals())


def delete(email, vault_name):
    return _call_az("az keyvault certificate contact delete", locals())

