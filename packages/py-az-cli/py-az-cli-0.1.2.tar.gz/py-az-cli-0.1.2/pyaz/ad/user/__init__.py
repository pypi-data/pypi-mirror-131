from ... pyaz_utils import call_az

def delete(id):
    return call_az("az ad user delete", locals())


def show(id):
    return call_az("az ad user show", locals())


def list(display_name=None, filter=None, upn=None):
    '''
    List Azure Active Directory users.
    '''
    return call_az("az ad user list", locals())


def get_member_groups(id, security_enabled_only=None):
    '''
    Get groups of which the user is a member
    '''
    return call_az("az ad user get-member-groups", locals())


def create(display_name, password, user_principal_name, force_change_password_next_login=None, immutable_id=None, mail_nickname=None):
    '''
    Create an Azure Active Directory user.
    '''
    return call_az("az ad user create", locals())


def update(id, account_enabled=None, display_name=None, force_change_password_next_login=None, mail_nickname=None, password=None):
    '''
    Update Azure Active Directory users.
    '''
    return call_az("az ad user update", locals())

