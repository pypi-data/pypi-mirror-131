from .... pyaz_utils import call_az
from . import admin


def update(issuer_name, vault_name, account_id=None, enabled=None, organization_id=None, password=None, provider_name=None):
    return call_az("az keyvault certificate issuer update", locals())


def list(vault_name, maxresults=None):
    return call_az("az keyvault certificate issuer list", locals())


def create(issuer_name, provider_name, vault_name, account_id=None, disabled=None, organization_id=None, password=None):
    return call_az("az keyvault certificate issuer create", locals())


def show(issuer_name, vault_name):
    return call_az("az keyvault certificate issuer show", locals())


def delete(issuer_name, vault_name):
    return call_az("az keyvault certificate issuer delete", locals())

