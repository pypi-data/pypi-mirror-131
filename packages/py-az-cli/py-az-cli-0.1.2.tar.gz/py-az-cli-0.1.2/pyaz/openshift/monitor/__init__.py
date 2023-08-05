from ... pyaz_utils import call_az

def enable(name, resource_group, workspace_id, no_wait=None):
    '''
    Enable Log Analytics monitoring in an ARO 3.11 cluster.
    '''
    return call_az("az openshift monitor enable", locals())


def disable(name, resource_group, no_wait=None):
    '''
    Disable Log Analytics monitoring in an ARO 3.11 cluster.
    '''
    return call_az("az openshift monitor disable", locals())

