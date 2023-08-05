from ... pyaz_utils import call_az
from . import commitment_plan, deployment, identity, keys, network_rule


def create(kind, location, name, resource_group, sku, api_properties=None, assign_identity=None, custom_domain=None, encryption=None, storage=None, tags=None, yes=None):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account create", locals())


def delete(name, resource_group):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account delete", locals())


def show(name, resource_group):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account show", locals())


def update(name, resource_group, api_properties=None, custom_domain=None, encryption=None, sku=None, storage=None, tags=None):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account update", locals())


def list(resource_group=None):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account list", locals())


def show_deleted(location, name, resource_group):
    '''
    Show a soft-deleted Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account show-deleted", locals())


def list_deleted():
    '''
    List soft-deleted Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account list-deleted", locals())


def purge(location, name, resource_group):
    '''
    Purge a soft-deleted Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account purge", locals())


def recover(location, name, resource_group):
    '''
    Recover a soft-deleted Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account recover", locals())


def list_skus(kind=None, location=None, name=None, resource_group=None):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices account list-skus", locals())


def list_usage(name, resource_group):
    return call_az("az cognitiveservices account list-usage", locals())


def list_kinds():
    return call_az("az cognitiveservices account list-kinds", locals())

