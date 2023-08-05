from ... pyaz_utils import call_az

def create(name, resource_group, location=None, tags=None, vnets=None):
    '''
    Create a DDoS protection plan.
    '''
    return call_az("az network ddos-protection create", locals())


def delete(name, resource_group):
    '''
    Delete a DDoS protection plan.
    '''
    return call_az("az network ddos-protection delete", locals())


def list(resource_group=None):
    '''
    List DDoS protection plans.
    '''
    return call_az("az network ddos-protection list", locals())


def show(name, resource_group):
    '''
    Show details of a DDoS protection plan.
    '''
    return call_az("az network ddos-protection show", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None, tags=None, vnets=None):
    '''
    Update a DDoS protection plan.
    '''
    return call_az("az network ddos-protection update", locals())

