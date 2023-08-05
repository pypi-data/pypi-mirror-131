from ..... pyaz_utils import call_az

def list(partner_namespace_name, resource_group):
    '''
    List shared access keys of a partner namespace.
    '''
    return call_az("az eventgrid partner namespace key list", locals())


def regenerate(key_name, partner_namespace_name, resource_group):
    '''
    Regenerate a shared access key of a partner namespace.
    '''
    return call_az("az eventgrid partner namespace key regenerate", locals())

