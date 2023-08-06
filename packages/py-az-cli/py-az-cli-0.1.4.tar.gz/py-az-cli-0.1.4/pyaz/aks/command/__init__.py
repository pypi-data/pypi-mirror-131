from ... pyaz_utils import _call_az

def invoke(name, resource_group, command=None, file=None, no_wait=None):
    '''
    Run a shell command (with kubectl, helm) on your aks cluster, support attaching files as well.
    '''
    return _call_az("az aks command invoke", locals())


def result(name, resource_group, command_id=None):
    '''
    Fetch result from previously triggered 'aks command invoke'.
    '''
    return _call_az("az aks command result", locals())

