from .... pyaz_utils import call_az

def set(managed_instance, name, resource_group, monthly_retention=None, week_of_year=None, weekly_retention=None, yearly_retention=None):
    '''
    Update long term retention settings for a managed database.
    '''
    return call_az("az sql midb ltr-policy set", locals())


def show(managed_instance, name, resource_group):
    '''
    Show the long term retention policy for a managed database.
    '''
    return call_az("az sql midb ltr-policy show", locals())

