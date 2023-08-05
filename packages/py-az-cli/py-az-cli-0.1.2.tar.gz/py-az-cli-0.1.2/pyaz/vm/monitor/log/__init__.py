from .... pyaz_utils import call_az

def show(analytics_query, name, resource_group, timespan=None):
    '''
    Execute a query against the Log Analytics workspace linked with a VM.
    '''
    return call_az("az vm monitor log show", locals())

