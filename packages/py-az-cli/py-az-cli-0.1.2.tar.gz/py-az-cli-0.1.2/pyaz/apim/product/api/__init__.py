from .... pyaz_utils import call_az

def list(product_id, resource_group, service_name):
    '''
    Lists a collection of the APIs associated with a product.
    '''
    return call_az("az apim product api list", locals())


def check(api_id, product_id, resource_group, service_name):
    '''
    Checks that API entity specified by identifier is associated with the Product entity.
    '''
    return call_az("az apim product api check", locals())


def add(api_id, product_id, resource_group, service_name):
    '''
    Add an API to the specified product.
    '''
    return call_az("az apim product api add", locals())


def delete(api_id, product_id, resource_group, service_name):
    '''
    Deletes the specified API from the specified product.
    '''
    return call_az("az apim product api delete", locals())

