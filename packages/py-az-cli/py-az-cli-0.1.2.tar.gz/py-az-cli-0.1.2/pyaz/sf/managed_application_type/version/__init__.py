from .... pyaz_utils import call_az

def list(cluster_name, name, resource_group):
    '''
    List versions of a given managed application type.
    '''
    return call_az("az sf managed-application-type version list", locals())


def delete(cluster_name, name, resource_group, version):
    '''
    Delete a managed application type version.
    '''
    return call_az("az sf managed-application-type version delete", locals())


def show(cluster_name, name, resource_group, version):
    '''
    Show the properties of a managed application type version on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-application-type version show", locals())


def create(cluster_name, name, package_url, resource_group, version, tags=None):
    '''
    Create a new managed application type on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-application-type version create", locals())


def update(cluster_name, name, resource_group, version, package_url=None, tags=None):
    '''
    Update a managed application type version.
    '''
    return call_az("az sf managed-application-type version update", locals())

