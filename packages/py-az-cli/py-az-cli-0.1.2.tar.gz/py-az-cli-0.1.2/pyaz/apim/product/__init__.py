from ... pyaz_utils import call_az
from . import api


def list(resource_group, service_name):
    '''
    Lists a collection of products in the specified service instance.
    '''
    return call_az("az apim product list", locals())


def show(product_id, resource_group, service_name):
    '''
    Gets the details of the product specified by its identifier.
    '''
    return call_az("az apim product show", locals())


def create(product_name, resource_group, service_name, approval_required=None, description=None, legal_terms=None, no_wait=None, product_id=None, state=None, subscription_required=None, subscriptions_limit=None):
    '''
    Creates a product.
    '''
    return call_az("az apim product create", locals())


def update(product_id, resource_group, service_name, add=None, approval_required=None, description=None, force_string=None, if_match=None, legal_terms=None, no_wait=None, product_name=None, remove=None, set=None, state=None, subscription_required=None, subscriptions_limit=None):
    '''
    Update existing product details.
    '''
    return call_az("az apim product update", locals())


def delete(product_id, resource_group, service_name, delete_subscriptions=None, if_match=None, no_wait=None, yes=None):
    '''
    Delete product.
    '''
    return call_az("az apim product delete", locals())


def wait(product_id, resource_group, service_name, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of an apim product is met.
    '''
    return call_az("az apim product wait", locals())

