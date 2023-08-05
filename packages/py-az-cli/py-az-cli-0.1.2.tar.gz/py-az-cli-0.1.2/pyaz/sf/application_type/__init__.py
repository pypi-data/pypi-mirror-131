from ... pyaz_utils import call_az
from . import version


def list(cluster_name, resource_group):
    '''
    List application types of a given cluster.
    '''
    return call_az("az sf application-type list", locals())


def delete(cluster_name, name, resource_group):
    '''
    Delete an application type.
    '''
    return call_az("az sf application-type delete", locals())


def show(cluster_name, name, resource_group):
    '''
    Show the properties of an application type on an Azure Service Fabric cluster.
    '''
    return call_az("az sf application-type show", locals())


def create(cluster_name, name, resource_group):
    '''
    Create a new application type on an Azure Service Fabric cluster.
    '''
    return call_az("az sf application-type create", locals())

