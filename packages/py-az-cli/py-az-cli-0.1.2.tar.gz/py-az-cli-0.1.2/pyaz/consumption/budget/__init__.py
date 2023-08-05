from ... pyaz_utils import call_az

def list(resource_group=None):
    '''
    List budgets for an Azure subscription.
    '''
    return call_az("az consumption budget list", locals())


def show(budget_name, resource_group=None):
    '''
    Show budget for an Azure subscription.
    '''
    return call_az("az consumption budget show", locals())


def create(amount, budget_name, category, end_date, start_date, time_grain, meter_filter=None, resource_filter=None, resource_group=None, resource_group_filter=None):
    '''
    Create a budget for an Azure subscription.
    '''
    return call_az("az consumption budget create", locals())


def delete(budget_name, resource_group=None):
    '''
    Delete a budget for an Azure subscription.
    '''
    return call_az("az consumption budget delete", locals())

