from .... pyaz_utils import call_az

def show(name, resource_group, deployment_id=None, slot=None):
    '''
    Show deployment logs of the latest deployment, or a specific deployment if deployment-id is specified.
    '''
    return call_az("az functionapp log deployment show", locals())


def list(name, resource_group, slot=None):
    '''
    List deployment logs of the deployments associated with function app
    '''
    return call_az("az functionapp log deployment list", locals())

