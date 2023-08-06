from ... pyaz_utils import _call_az

def list(location):
    '''
    Show all commitment tiers for Azure Cognitive Services.
    '''
    return _call_az("az cognitiveservices commitment-tier list", locals())

