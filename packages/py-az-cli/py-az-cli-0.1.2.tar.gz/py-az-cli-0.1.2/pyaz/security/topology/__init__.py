from ... pyaz_utils import call_az

def list():
    '''
    Shows the network topology in your subscription.
    '''
    return call_az("az security topology list", locals())


def show(name, resource_group):
    '''
    Shows the network topology in your subscription.
    '''
    return call_az("az security topology show", locals())

