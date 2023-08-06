from ..... pyaz_utils import _call_az

def list():
    '''
    List ExpressRoute port locations.
    '''
    return _call_az("az network express-route port location list", locals())


def show(location):
    '''
    Get the details of an ExpressRoute port location.
    '''
    return _call_az("az network express-route port location show", locals())

