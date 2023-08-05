from ... pyaz_utils import call_az
from . import create, update


def list(name=None, resource_group=None, source_id=None):
    '''
    List connections of a webapp.
    '''
    return call_az("az webapp connection list", locals())


def show(connection=None, id=None, name=None, resource_group=None):
    '''
    Get the details of a webapp connection.
    '''
    return call_az("az webapp connection show", locals())


def delete(connection=None, id=None, name=None, no_wait=None, resource_group=None, yes=None):
    '''
    Delete a webapp connection.
    '''
    return call_az("az webapp connection delete", locals())


def list_configuration(connection=None, id=None, name=None, resource_group=None):
    '''
    List source configurations of a webapp connection.
    '''
    return call_az("az webapp connection list-configuration", locals())


def validate(connection=None, id=None, name=None, resource_group=None):
    '''
    Validate a webapp connection.
    '''
    return call_az("az webapp connection validate", locals())


def list_support_types(target_type=None):
    '''
    List client types and auth types supported by webapp connections.
    '''
    return call_az("az webapp connection list-support-types", locals())


def wait(connection=None, created=None, custom=None, deleted=None, exists=None, id=None, interval=None, name=None, resource_group=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the connection is met.
    '''
    return call_az("az webapp connection wait", locals())

