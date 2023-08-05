from ... pyaz_utils import call_az
from . import terms


def list_offers(location, publisher, edge_zone=None):
    '''
    List the VM image offers available in the Azure Marketplace.
    '''
    return call_az("az vm image list-offers", locals())


def list_publishers(location, edge_zone=None):
    '''
    List the VM image publishers available in the Azure Marketplace.
    '''
    return call_az("az vm image list-publishers", locals())


def list_skus(location, offer, publisher, edge_zone=None):
    '''
    List the VM image SKUs available in the Azure Marketplace.
    '''
    return call_az("az vm image list-skus", locals())


def list(all=None, edge_zone=None, location=None, offer=None, publisher=None, sku=None):
    '''
    List the VM/VMSS images available in the Azure Marketplace.
    '''
    return call_az("az vm image list", locals())


def accept_terms(offer=None, plan=None, publisher=None, urn=None):
    '''
    Accept Azure Marketplace term so that the image can be used to create VMs
    '''
    return call_az("az vm image accept-terms", locals())


def show(edge_zone=None, location=None, offer=None, publisher=None, sku=None, urn=None, version=None):
    '''
    Get the details for a VM image available in the Azure Marketplace.
    '''
    return call_az("az vm image show", locals())

