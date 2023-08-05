from ... pyaz_utils import call_az

def list():
    '''
    Lists available operations for the Kusto sub-resources inside Microsoft.Synapse provider.
    '''
    return call_az("az synapse kusto-operation list", locals())

