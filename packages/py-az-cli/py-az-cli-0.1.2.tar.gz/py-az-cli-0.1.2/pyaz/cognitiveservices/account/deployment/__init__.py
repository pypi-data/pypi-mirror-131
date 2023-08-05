from .... pyaz_utils import call_az

def create(model_format, model_name, model_version, name, resource_group, scale_capacity, scale_type, deployment_name=None):
    '''
    Create a deployment for Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account deployment create", locals())


def delete(name, resource_group, deployment_name=None):
    '''
    Delete a deployment from Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account deployment delete", locals())


def show(name, resource_group, deployment_name=None):
    '''
    Show a deployment for Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account deployment show", locals())


def list(name, resource_group):
    '''
    Show all deployments for Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account deployment list", locals())

