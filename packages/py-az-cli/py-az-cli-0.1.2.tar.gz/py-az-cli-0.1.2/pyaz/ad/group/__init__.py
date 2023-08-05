from ... pyaz_utils import call_az
from . import member, owner


def delete(group):
    return call_az("az ad group delete", locals())


def show(group):
    return call_az("az ad group show", locals())


def get_member_groups(group, additional_properties=None, security_enabled_only=None):
    return call_az("az ad group get-member-groups", locals())


def list(display_name=None, filter=None):
    return call_az("az ad group list", locals())


def create(display_name, mail_nickname, description=None, force=None):
    '''
    Create a group in the directory.
    '''
    return call_az("az ad group create", locals())

