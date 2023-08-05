from .... pyaz_utils import call_az

def check_dns(name, type=None):
    '''
    Check the availability of a relative DNS name.
    '''
    return call_az("az network traffic-manager profile check-dns", locals())


def show(name, resource_group):
    '''
    Get the details of a traffic manager profile.
    '''
    return call_az("az network traffic-manager profile show", locals())


def delete(name, resource_group):
    '''
    Delete a traffic manager profile.
    '''
    return call_az("az network traffic-manager profile delete", locals())


def list(resource_group=None):
    '''
    List traffic manager profiles.
    '''
    return call_az("az network traffic-manager profile list", locals())


def create(name, resource_group, routing_method, unique_dns_name, custom_headers=None, interval=None, max_failures=None, max_return=None, path=None, port=None, protocol=None, status=None, status_code_ranges=None, tags=None, timeout=None, ttl=None):
    '''
    Create a traffic manager profile.
    '''
    return call_az("az network traffic-manager profile create", locals())


def update(name, resource_group, add=None, custom_headers=None, force_string=None, interval=None, max_failures=None, max_return=None, path=None, port=None, protocol=None, remove=None, routing_method=None, set=None, status=None, status_code_ranges=None, tags=None, timeout=None, ttl=None):
    '''
    Update a traffic manager profile.
    '''
    return call_az("az network traffic-manager profile update", locals())

