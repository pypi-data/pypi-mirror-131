from .... pyaz_utils import call_az

def info(name, parent_protocol, registry, resource_group=None):
    '''
    Retrieve information required to activate a connected registry.
    '''
    return call_az("az acr connected-registry install info", locals())


def renew_credentials(name, parent_protocol, registry, resource_group=None, yes=None):
    '''
    Retrieve information required to activate a connected registry, and renews the sync token credentials.
    '''
    return call_az("az acr connected-registry install renew-credentials", locals())

