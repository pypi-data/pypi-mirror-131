from .... pyaz_utils import call_az

def delete(name, registry, password1=None, password2=None, resource_group=None):
    '''
    Delete a token credential.
    '''
    return call_az("az acr token credential delete", locals())


def generate(name, registry, expiration=None, expiration_in_days=None, password1=None, password2=None, resource_group=None):
    '''
    Generate or replace one or both passwords of a token for an Azure Container Registry. For using token and password to access a container registry, see https://aka.ms/acr/repo-permissions.
    '''
    return call_az("az acr token credential generate", locals())

