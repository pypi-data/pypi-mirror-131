from .... pyaz_utils import call_az

def create(account_name, name, sas_type, template_uri, validity_period, vault_name, disabled=None, tags=None):
    return call_az("az keyvault storage sas-definition create", locals())


def list(account_name, vault_name, maxresults=None):
    return call_az("az keyvault storage sas-definition list", locals())


def show(account_name=None, id=None, name=None, vault_name=None):
    return call_az("az keyvault storage sas-definition show", locals())


def update(account_name=None, disabled=None, id=None, name=None, sas_type=None, tags=None, template_uri=None, validity_period=None, vault_name=None):
    return call_az("az keyvault storage sas-definition update", locals())


def delete(account_name=None, id=None, name=None, vault_name=None):
    return call_az("az keyvault storage sas-definition delete", locals())


def list_deleted(account_name, vault_name, maxresults=None):
    return call_az("az keyvault storage sas-definition list-deleted", locals())


def show_deleted(account_name, name, vault_name):
    return call_az("az keyvault storage sas-definition show-deleted", locals())


def recover(account_name, name, vault_name):
    return call_az("az keyvault storage sas-definition recover", locals())

