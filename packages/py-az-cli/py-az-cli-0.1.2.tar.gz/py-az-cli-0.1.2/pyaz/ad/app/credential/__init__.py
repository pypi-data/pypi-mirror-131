from .... pyaz_utils import call_az

def reset(id, append=None, cert=None, create_cert=None, credential_description=None, end_date=None, keyvault=None, password=None, years=None):
    '''
    Append or overwrite an application's password or certificate credentials
    '''
    return call_az("az ad app credential reset", locals())


def list(id, cert=None):
    '''
    List an application's password or certificate credential metadata. (The content of the password or certificate credential is not retrievable.)
    '''
    return call_az("az ad app credential list", locals())


def delete(id, key_id, cert=None):
    '''
    delete an application's password or certificate credentials
    '''
    return call_az("az ad app credential delete", locals())

