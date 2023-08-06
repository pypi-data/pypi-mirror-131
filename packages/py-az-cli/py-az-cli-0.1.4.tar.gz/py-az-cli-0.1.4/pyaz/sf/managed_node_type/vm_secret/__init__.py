from .... pyaz_utils import _call_az

def add(certificate_store, certificate_url, cluster_name, resource_group, source_vault_id):
    '''
    Add a secret to the node type.
    '''
    return _call_az("az sf managed-node-type vm-secret add", locals())

