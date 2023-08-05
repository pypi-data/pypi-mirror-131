from .... pyaz_utils import call_az

def create(auto_renew, commitment_plan_name, hosting_model, name, plan_type, resource_group, current_count=None, current_tier=None, next_count=None, next_tier=None):
    '''
    Create a commitment plan for Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account commitment-plan create", locals())


def delete(commitment_plan_name, name, resource_group):
    '''
    Delete a commitment plan from Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account commitment-plan delete", locals())


def show(commitment_plan_name, name, resource_group):
    '''
    Show a commitment plan from Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account commitment-plan show", locals())


def list(name, resource_group):
    '''
    Show all commitment plans from Azure Cognitive Services account.
    '''
    return call_az("az cognitiveservices account commitment-plan list", locals())

