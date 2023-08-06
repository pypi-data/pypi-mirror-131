from .. pyaz_utils import _call_az

def show(plan, product, publisher):
    '''
    Get marketplace terms.
    '''
    return _call_az("az term show", locals())


def accept(plan, product, publisher):
    '''
    Accept marketplace terms.
    '''
    return _call_az("az term accept", locals())

