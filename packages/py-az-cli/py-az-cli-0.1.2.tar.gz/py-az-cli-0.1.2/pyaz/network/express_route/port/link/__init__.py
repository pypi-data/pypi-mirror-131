from ..... pyaz_utils import call_az

def list(port_name, resource_group):
    '''
    List ExpressRoute links.
    '''
    return call_az("az network express-route port link list", locals())


def show(name, port_name, resource_group):
    '''
    Get the details of an ExpressRoute link.
    '''
    return call_az("az network express-route port link show", locals())


def update(name, port_name, resource_group, add=None, admin_state=None, force_string=None, macsec_cak_secret_identifier=None, macsec_cipher=None, macsec_ckn_secret_identifier=None, macsec_sci_state=None, no_wait=None, remove=None, set=None):
    '''
    Manage MACsec configuration of an ExpressRoute Link.
    '''
    return call_az("az network express-route port link update", locals())

