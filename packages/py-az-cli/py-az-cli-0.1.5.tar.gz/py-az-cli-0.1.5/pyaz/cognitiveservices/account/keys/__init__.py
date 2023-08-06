from .... pyaz_utils import _call_az

def regenerate(key_name, name, resource_group):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return _call_az("az cognitiveservices account keys regenerate", locals())


def list(name, resource_group):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return _call_az("az cognitiveservices account keys list", locals())

