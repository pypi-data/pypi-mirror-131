from ... pyaz_utils import call_az
from . import profile, rule


def create(count, resource, action=None, disabled=None, email_administrator=None, email_coadministrators=None, location=None, max_count=None, min_count=None, name=None, resource_group=None, resource_namespace=None, resource_parent=None, resource_type=None, tags=None):
    '''
    Create new autoscale settings.
    '''
    return call_az("az monitor autoscale create", locals())


def update(name, resource_group, add=None, add_action=None, count=None, email_administrator=None, email_coadministrators=None, enabled=None, force_string=None, max_count=None, min_count=None, remove=None, remove_action=None, set=None, tags=None):
    '''
    Update autoscale settings.
    '''
    return call_az("az monitor autoscale update", locals())


def delete(name, resource_group):
    return call_az("az monitor autoscale delete", locals())


def show(name, resource_group):
    '''
    Show autoscale setting details.
    '''
    return call_az("az monitor autoscale show", locals())


def list(resource_group):
    return call_az("az monitor autoscale list", locals())

