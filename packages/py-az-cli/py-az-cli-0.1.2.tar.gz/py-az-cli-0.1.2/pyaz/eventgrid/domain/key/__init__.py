from .... pyaz_utils import call_az

def list(name, resource_group):
    '''
    List shared access keys of a domain.
    '''
    return call_az("az eventgrid domain key list", locals())


def regenerate(key_name, name, resource_group):
    '''
    Regenerate a shared access key of a domain.
    '''
    return call_az("az eventgrid domain key regenerate", locals())

