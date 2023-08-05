from .... pyaz_utils import call_az

def set_permission(account, path, permission):
    '''
    Set the permissions for a file or folder in a Data Lake Store account.
    '''
    return call_az("az dls fs access set-permission", locals())


def set_owner(account, path, group=None, owner=None):
    '''
    Set the owner information for a file or folder in a Data Lake Store account.
    '''
    return call_az("az dls fs access set-owner", locals())


def show(account, path):
    '''
    Display the access control list (ACL).
    '''
    return call_az("az dls fs access show", locals())


def set_entry(account, acl_spec, path):
    '''
    Update the access control list for a file or folder.
    '''
    return call_az("az dls fs access set-entry", locals())


def set(account, acl_spec, path):
    '''
    Replace the existing access control list for a file or folder.
    '''
    return call_az("az dls fs access set", locals())


def remove_entry(account, acl_spec, path):
    '''
    Remove entries for the access control list of a file or folder.
    '''
    return call_az("az dls fs access remove-entry", locals())


def remove_all(account, path, default_acl=None):
    '''
    Remove the access control list for a file or folder.
    '''
    return call_az("az dls fs access remove-all", locals())

