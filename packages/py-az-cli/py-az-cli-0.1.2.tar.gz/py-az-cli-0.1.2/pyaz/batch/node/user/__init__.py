from .... pyaz_utils import call_az

def create(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, expiry_time=None, is_admin=None, json_file=None, name=None, password=None, ssh_public_key=None):
    '''
    Add a user account to a Batch compute node.
    '''
    return call_az("az batch node user create", locals())


def delete(node_id, pool_id, user_name, account_endpoint=None, account_key=None, account_name=None, yes=None):
    return call_az("az batch node user delete", locals())


def reset(node_id, pool_id, user_name, account_endpoint=None, account_key=None, account_name=None, expiry_time=None, json_file=None, password=None, ssh_public_key=None):
    '''
    Update the properties of a user account on a Batch compute node. Unspecified properties which can be updated are reset to their defaults.
    '''
    return call_az("az batch node user reset", locals())

