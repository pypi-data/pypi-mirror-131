from ..... pyaz_utils import call_az

def list(resource_group, workspace_name):
    '''
    List all the intelligence packs possible and whether they are enabled or disabled for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace pack list", locals())


def enable(name, resource_group, workspace_name):
    '''
    Enable an intelligence pack for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace pack enable", locals())


def disable(name, resource_group, workspace_name):
    '''
    Disable an intelligence pack for a given workspace.
    '''
    return call_az("az monitor log-analytics workspace pack disable", locals())

