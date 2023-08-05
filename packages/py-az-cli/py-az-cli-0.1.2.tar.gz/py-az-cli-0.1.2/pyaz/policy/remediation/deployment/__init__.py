from .... pyaz_utils import call_az

def list(name, management_group=None, namespace=None, parent=None, resource=None, resource_group=None, resource_type=None):
    '''
    Lists deployments for a resource policy remediation.
    '''
    return call_az("az policy remediation deployment list", locals())

