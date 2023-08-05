from .... pyaz_utils import call_az

def create(account, compute_policy_name, object_id, object_type, max_dop_per_job=None, min_priority_per_job=None, resource_group=None):
    '''
    Create a compute policy in the Data Lake Analytics account.
    '''
    return call_az("az dla account compute-policy create", locals())


def update(account, compute_policy_name, max_dop_per_job=None, min_priority_per_job=None, resource_group=None):
    '''
    Update a compute policy in the Data Lake Analytics account.
    '''
    return call_az("az dla account compute-policy update", locals())


def list(account, resource_group=None):
    '''
    List compute policies in the a Lake Analytics account.
    '''
    return call_az("az dla account compute-policy list", locals())


def show(account, compute_policy_name, resource_group=None):
    '''
    Retrieve a compute policy in a Data Lake Analytics account.
    '''
    return call_az("az dla account compute-policy show", locals())


def delete(account, compute_policy_name, resource_group=None):
    '''
    Delete a compute policy in a Data Lake Analytics account.
    '''
    return call_az("az dla account compute-policy delete", locals())

