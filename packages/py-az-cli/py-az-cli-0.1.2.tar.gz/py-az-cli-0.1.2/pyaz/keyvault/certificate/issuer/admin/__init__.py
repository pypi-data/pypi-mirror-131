from ..... pyaz_utils import call_az

def list(issuer_name, vault_name):
    return call_az("az keyvault certificate issuer admin list", locals())


def add(email, issuer_name, vault_name, first_name=None, last_name=None, phone=None):
    return call_az("az keyvault certificate issuer admin add", locals())


def delete(email, issuer_name, vault_name):
    return call_az("az keyvault certificate issuer admin delete", locals())

