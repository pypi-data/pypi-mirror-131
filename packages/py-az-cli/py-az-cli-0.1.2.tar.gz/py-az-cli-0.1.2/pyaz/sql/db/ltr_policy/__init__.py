from .... pyaz_utils import call_az

def set(name, resource_group, server, monthly_retention=None, week_of_year=None, weekly_retention=None, yearly_retention=None):
    '''
    Update long term retention settings for a database.
    '''
    return call_az("az sql db ltr-policy set", locals())


def show(name, resource_group, server):
    '''
    Show the long term retention policy for a database.
    '''
    return call_az("az sql db ltr-policy show", locals())

