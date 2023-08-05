from ... pyaz_utils import call_az

def list():
    '''
    list of all possible traffic between resources for the subscription.
    '''
    return call_az("az security allowed_connections list", locals())


def show(name, resource_group):
    '''
    List all possible traffic between resources for the subscription and location, based on connection type.
    '''
    return call_az("az security allowed_connections show", locals())

