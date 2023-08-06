from ... pyaz_utils import _call_az

def list(name, resource_group=None):
    '''
    List access keys of an App Configuration.
    '''
    return _call_az("az appconfig credential list", locals())


def regenerate(id, name, resource_group=None):
    '''
    Regenerate an access key for an App Configuration.
    '''
    return _call_az("az appconfig credential regenerate", locals())

