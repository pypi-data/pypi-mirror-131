from .... pyaz_utils import call_az

def create(application, cluster_name, metric_name, name, resource_group, default_load=None, primary_default_load=None, secondary_default_load=None, weight=None):
    '''
    Create a new managed service load metric on an Azure Service Fabric managed cluster.
    '''
    return call_az("az sf managed-service load-metrics create", locals())


def update(application, cluster_name, metric_name, name, resource_group, default_load=None, primary_default_load=None, secondary_default_load=None, weight=None):
    '''
    Update a managed service.
    '''
    return call_az("az sf managed-service load-metrics update", locals())


def delete(application, cluster_name, metric_name, name, resource_group):
    '''
    Delete a managed service.
    '''
    return call_az("az sf managed-service load-metrics delete", locals())

