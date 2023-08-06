from ... pyaz_utils import _call_az

def list_operation():
    '''
    List operations available for the Maps Resource Provider.
    '''
    return _call_az("az maps map list-operation", locals())

