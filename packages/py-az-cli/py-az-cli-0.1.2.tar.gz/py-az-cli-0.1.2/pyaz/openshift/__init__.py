from .. pyaz_utils import call_az
from . import monitor


def create(name, resource_group, aad_client_app_id=None, aad_client_app_secret=None, aad_tenant_id=None, compute_count=None, compute_vm_size=None, customer_admin_group_id=None, location=None, no_wait=None, subnet_prefix=None, tags=None, vnet_peer=None, vnet_prefix=None, workspace_id=None):
    '''
    Create a new Azure Red Hat OpenShift 3.11 cluster.
    '''
    return call_az("az openshift create", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete an Azure Red Hat OpenShift 3.11 cluster.
    '''
    return call_az("az openshift delete", locals())


def scale(compute_count, name, resource_group, no_wait=None):
    '''
    Scale the compute pool in an Azure Red Hat OpenShift 3.11 cluster.
    '''
    return call_az("az openshift scale", locals())


def show(name, resource_group):
    '''
    Show the details for an Azure Red Hat OpenShift 3.11 cluster.
    '''
    return call_az("az openshift show", locals())


def list(resource_group=None):
    '''
    List Azure Red Hat OpenShift 3.11 clusters.
    '''
    return call_az("az openshift list", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for an Azure Red Hat OpenShift 3.11 cluster to reach a desired state.
    '''
    return call_az("az openshift wait", locals())

