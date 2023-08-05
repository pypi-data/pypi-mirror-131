from ... pyaz_utils import call_az

def list_operation():
    '''
    List operations available for the Maps Resource Provider.
    '''
    return call_az("az maps map list-operation", locals())

