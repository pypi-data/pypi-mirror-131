from .... pyaz_utils import call_az

def show(name, resource_group, deployment_id=None, slot=None):
    '''
    Show deployment logs of the latest deployment, or a specific deployment if deployment-id is specified.
    '''
    return call_az("az webapp log deployment show", locals())


def list(name, resource_group, slot=None):
    '''
    List deployments associated with web app
    '''
    return call_az("az webapp log deployment list", locals())

