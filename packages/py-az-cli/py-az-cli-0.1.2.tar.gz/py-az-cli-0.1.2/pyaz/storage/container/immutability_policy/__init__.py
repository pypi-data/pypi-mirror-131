from .... pyaz_utils import call_az

def show(account_name, container_name, if_match=None, resource_group=None):
    return call_az("az storage container immutability-policy show", locals())


def create(account_name, container_name, allow_protected_append_writes=None, allow_protected_append_writes_all=None, if_match=None, period=None, resource_group=None):
    '''
    Create or update an unlocked immutability policy.
    '''
    return call_az("az storage container immutability-policy create", locals())


def delete(account_name, container_name, if_match, resource_group=None):
    return call_az("az storage container immutability-policy delete", locals())


def lock(account_name, container_name, if_match, resource_group=None):
    return call_az("az storage container immutability-policy lock", locals())


def extend(account_name, container_name, if_match, allow_protected_append_writes=None, allow_protected_append_writes_all=None, period=None, resource_group=None):
    '''
    Extend the immutabilityPeriodSinceCreationInDays of a locked immutabilityPolicy.
    '''
    return call_az("az storage container immutability-policy extend", locals())

