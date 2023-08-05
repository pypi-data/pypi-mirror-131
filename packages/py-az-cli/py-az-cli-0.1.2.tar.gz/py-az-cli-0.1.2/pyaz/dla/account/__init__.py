from ... pyaz_utils import call_az
from . import blob_storage, compute_policy, data_lake_store, firewall


def create(account, default_data_lake_store, location=None, max_degree_of_parallelism=None, max_job_count=None, query_store_retention=None, resource_group=None, tags=None, tier=None):
    '''
    Create a Data Lake Analytics account.
    '''
    return call_az("az dla account create", locals())


def update(account, allow_azure_ips=None, firewall_state=None, max_degree_of_parallelism=None, max_job_count=None, query_store_retention=None, resource_group=None, tags=None, tier=None):
    '''
    Update a Data Lake Analytics account.
    '''
    return call_az("az dla account update", locals())


def list(resource_group=None):
    '''
    List available Data Lake Analytics accounts.
    '''
    return call_az("az dla account list", locals())


def show(account, resource_group=None):
    '''
    Get the details of a Data Lake Analytics account.
    '''
    return call_az("az dla account show", locals())


def delete(account, resource_group=None):
    '''
    Delete a Data Lake Analytics account.
    '''
    return call_az("az dla account delete", locals())

