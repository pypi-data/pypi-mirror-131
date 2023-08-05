from ... pyaz_utils import call_az

def list(name, authentication_provider=None, resource_group=None):
    '''
    Lists users and assigned roles, limited to users who accepted their invites.
    '''
    return call_az("az staticwebapp users list", locals())


def invite(authentication_provider, domain, invitation_expiration_in_hours, name, roles, user_details, resource_group=None):
    '''
    Create invitation link for specified user to the static app.
    '''
    return call_az("az staticwebapp users invite", locals())


def update(name, roles, authentication_provider=None, resource_group=None, user_details=None, user_id=None):
    '''
    Updates a user entry with the listed roles. Either user details or user id is required.
    '''
    return call_az("az staticwebapp users update", locals())

