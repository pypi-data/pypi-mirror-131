from .. pyaz_utils import call_az
from . import account, commitment_tier


def list(resource_group=None):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return call_az("az cognitiveservices list", locals())

