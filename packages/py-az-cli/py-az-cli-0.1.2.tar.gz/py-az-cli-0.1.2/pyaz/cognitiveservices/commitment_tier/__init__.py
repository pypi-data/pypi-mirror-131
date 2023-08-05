from ... pyaz_utils import call_az

def list(location):
    '''
    Show all commitment tiers for Azure Cognitive Services.
    '''
    return call_az("az cognitiveservices commitment-tier list", locals())

