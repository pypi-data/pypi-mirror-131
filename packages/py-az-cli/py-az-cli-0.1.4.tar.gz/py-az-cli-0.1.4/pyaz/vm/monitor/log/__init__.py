from .... pyaz_utils import _call_az

def show(analytics_query, name, resource_group, timespan=None):
    '''
    Execute a query against the Log Analytics workspace linked with a VM.
    '''
    return _call_az("az vm monitor log show", locals())

