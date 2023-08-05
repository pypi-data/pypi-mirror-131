from .... pyaz_utils import call_az
from . import ag_listener


def update(name, resource_group, add=None, bootstrap_acc=None, domain_fqdn=None, force_string=None, fsw_path=None, operator_acc=None, ou_path=None, remove=None, sa_key=None, service_acc=None, set=None, storage_account=None, tags=None):
    '''
    Updates a SQL virtual machine group if there are not SQL virtual machines attached to the group.
    '''
    return call_az("az sql vm group update", locals())


def show(name, resource_group):
    return call_az("az sql vm group show", locals())


def list(resource_group=None):
    return call_az("az sql vm group list", locals())


def delete(name, resource_group, yes=None):
    return call_az("az sql vm group delete", locals())


def create(domain_fqdn, image_offer, image_sku, name, operator_acc, resource_group, service_acc, storage_account, bootstrap_acc=None, fsw_path=None, location=None, ou_path=None, sa_key=None, tags=None):
    '''
    Creates a SQL virtual machine group.
    '''
    return call_az("az sql vm group create", locals())

