from .... pyaz_utils import _call_az

def create(application, cluster_name, correlated_service_name, name, resource_group, scheme):
    '''
    Create a new managed service correlation scheme on an Azure Service Fabric managed cluster.
    '''
    return _call_az("az sf managed-service correlation-scheme create", locals())


def update(application, cluster_name, correlated_service_name, name, resource_group, scheme):
    '''
    Update a managed service correlation scheme.
    '''
    return _call_az("az sf managed-service correlation-scheme update", locals())


def delete(application, cluster_name, correlated_service_name, name, resource_group):
    '''
    Delete a managed service correlation scheme.
    '''
    return _call_az("az sf managed-service correlation-scheme delete", locals())

