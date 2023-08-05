from .... pyaz_utils import call_az

def reset(name, append=None, cert=None, create_cert=None, credential_description=None, end_date=None, keyvault=None, password=None, years=None):
    '''
    Reset a service principal credential.
    '''
    return call_az("az ad sp credential reset", locals())


def list(id, cert=None):
    '''
    List a service principal's credentials.
    '''
    return call_az("az ad sp credential list", locals())


def delete(id, key_id, cert=None):
    '''
    Delete a service principal's credential.
    '''
    return call_az("az ad sp credential delete", locals())

