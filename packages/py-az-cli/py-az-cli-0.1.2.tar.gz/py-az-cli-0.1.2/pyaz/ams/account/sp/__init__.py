from .... pyaz_utils import call_az

def create(account_name, resource_group, name=None, new_sp_name=None, password=None, role=None, xml=None, years=None):
    '''
    Create or update a service principal and configure its access to an Azure Media Services account.
    '''
    return call_az("az ams account sp create", locals())


def reset_credentials(account_name, resource_group, name=None, password=None, role=None, xml=None, years=None):
    '''
    Generate a new client secret for a service principal configured for an Azure Media Services account.
    '''
    return call_az("az ams account sp reset-credentials", locals())

