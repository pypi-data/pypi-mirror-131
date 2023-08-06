from .... pyaz_utils import _call_az

def list(name, resource_group):
    '''
    List shared access keys of a topic.
    '''
    return _call_az("az eventgrid topic key list", locals())


def regenerate(key_name, name, resource_group):
    '''
    Regenerate a shared access key of a topic.
    '''
    return _call_az("az eventgrid topic key regenerate", locals())

