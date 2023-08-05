from ... pyaz_utils import call_az
from . import version


def list(cluster_name, resource_group):
    '''
    List managed application types of a given managed cluster.
    '''
    return call_az("az sf managed-application-type list", locals())


def delete(cluster_name, name, resource_group):
    '''
    Delete a managed application type.
    '''
    return call_az("az sf managed-application-type delete", locals())


def show(cluster_name, name, resource_group):
    '''
    Show the properties of a managed application type on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-application-type show", locals())


def create(cluster_name, name, resource_group, tags=None):
    '''
    Create a new managed application type on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-application-type create", locals())


def update(cluster_name, name, resource_group, tags=None):
    '''
    Update an managed application type.
    '''
    return call_az("az sf managed-application-type update", locals())

