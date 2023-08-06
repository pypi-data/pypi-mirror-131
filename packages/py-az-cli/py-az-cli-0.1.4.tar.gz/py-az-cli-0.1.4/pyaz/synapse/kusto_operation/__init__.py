from ... pyaz_utils import _call_az

def list():
    '''
    Lists available operations for the Kusto sub-resources inside Microsoft.Synapse provider.
    '''
    return _call_az("az synapse kusto-operation list", locals())

