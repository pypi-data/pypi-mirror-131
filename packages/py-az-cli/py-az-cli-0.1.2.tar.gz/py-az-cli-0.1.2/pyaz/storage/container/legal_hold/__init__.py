from .... pyaz_utils import call_az

def set(account_name, container_name, tags, allow_protected_append_writes_all=None, resource_group=None):
    '''
    Set legal hold tags.
    '''
    return call_az("az storage container legal-hold set", locals())


def clear(account_name, container_name, tags, allow_protected_append_writes_all=None, resource_group=None):
    '''
    Clear legal hold tags.
    '''
    return call_az("az storage container legal-hold clear", locals())


def show(account_name, container_name, resource_group=None):
    '''
    Get the legal hold properties of a container.
    '''
    return call_az("az storage container legal-hold show", locals())

