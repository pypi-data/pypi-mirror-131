from .. pyaz_utils import _call_az
from . import account, commitment_tier


def list(resource_group=None):
    '''
    Manage Azure Cognitive Services accounts.
    '''
    return _call_az("az cognitiveservices list", locals())

