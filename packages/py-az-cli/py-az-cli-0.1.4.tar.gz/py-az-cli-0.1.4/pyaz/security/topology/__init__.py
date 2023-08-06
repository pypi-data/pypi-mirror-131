from ... pyaz_utils import _call_az

def list():
    '''
    Shows the network topology in your subscription.
    '''
    return _call_az("az security topology list", locals())


def show(name, resource_group):
    '''
    Shows the network topology in your subscription.
    '''
    return _call_az("az security topology show", locals())

