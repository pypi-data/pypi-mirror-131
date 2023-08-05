from .... pyaz_utils import call_az

def add(name, password=None, repository=None, resource_group=None, suffix=None, username=None):
    '''
    Add a helm chart repository from an Azure Container Registry through the Helm CLI.
    '''
    return call_az("az acr helm repo add", locals())

