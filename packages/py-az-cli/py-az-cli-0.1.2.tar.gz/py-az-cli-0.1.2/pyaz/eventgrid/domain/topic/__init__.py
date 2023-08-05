from .... pyaz_utils import call_az

def show(domain_name, name, resource_group):
    '''
    Get the details of a domain topic.
    '''
    return call_az("az eventgrid domain topic show", locals())


def list(domain_name, resource_group, odata_query=None):
    '''
    List available topics in a domain.
    '''
    return call_az("az eventgrid domain topic list", locals())


def delete(domain_name, name, resource_group):
    '''
    Delete a domain topic under a domain.
    '''
    return call_az("az eventgrid domain topic delete", locals())


def create(domain_name, name, resource_group):
    '''
    Create a domain topic under a domain.
    '''
    return call_az("az eventgrid domain topic create", locals())

