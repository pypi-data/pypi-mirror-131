from ... pyaz_utils import call_az

def show(name, resource_group=None):
    '''
    Get the login credentials for an Azure Container Registry.
    '''
    return call_az("az acr credential show", locals())


def renew(name, password_name, resource_group=None):
    '''
    Regenerate login credentials for an Azure Container Registry.
    '''
    return call_az("az acr credential renew", locals())

