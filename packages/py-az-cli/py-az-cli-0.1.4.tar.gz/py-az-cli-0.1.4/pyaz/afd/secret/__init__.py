from ... pyaz_utils import _call_az

def show(profile_name, resource_group, secret_name):
    return _call_az("az afd secret show", locals())


def delete(profile_name, resource_group, secret_name, yes=None):
    return _call_az("az afd secret delete", locals())


def list(profile_name, resource_group):
    return _call_az("az afd secret list", locals())


def create(profile_name, resource_group, secret_name, secret_source, secret_version=None, use_latest_version=None):
    '''
    Creates a new secret within the specified profile.
    '''
    return _call_az("az afd secret create", locals())


def update(profile_name, resource_group, secret_name, secret_source=None, secret_version=None, use_latest_version=None):
    '''
    Update an existing secret within the specified profile.
    '''
    return _call_az("az afd secret update", locals())

