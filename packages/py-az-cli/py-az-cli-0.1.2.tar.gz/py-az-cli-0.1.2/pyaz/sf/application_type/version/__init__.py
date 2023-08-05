from .... pyaz_utils import call_az

def list(cluster_name, name, resource_group):
    '''
    List version of a given application type.
    '''
    return call_az("az sf application-type version list", locals())


def delete(cluster_name, name, resource_group, version):
    '''
    Delete an application type version.
    '''
    return call_az("az sf application-type version delete", locals())


def show(cluster_name, name, resource_group, version):
    '''
    Show the properties of an application type version on an Azure Service Fabric cluster.
    '''
    return call_az("az sf application-type version show", locals())


def create(cluster_name, name, package_url, resource_group, version):
    '''
    Create a new application type on an Azure Service Fabric cluster.
    '''
    return call_az("az sf application-type version create", locals())

