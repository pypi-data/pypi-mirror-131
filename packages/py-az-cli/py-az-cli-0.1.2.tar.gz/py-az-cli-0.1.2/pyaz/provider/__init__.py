from .. pyaz_utils import call_az
from . import operation, permission


def list(expand=None):
    return call_az("az provider list", locals())


def show(namespace, expand=None):
    return call_az("az provider show", locals())


def register(namespace, accept_terms=None, consent_to_permissions=None, management_group_id=None, wait=None):
    '''
    Register a provider.
    '''
    return call_az("az provider register", locals())


def unregister(namespace, wait=None):
    '''
    Unregister a provider.
    '''
    return call_az("az provider unregister", locals())

