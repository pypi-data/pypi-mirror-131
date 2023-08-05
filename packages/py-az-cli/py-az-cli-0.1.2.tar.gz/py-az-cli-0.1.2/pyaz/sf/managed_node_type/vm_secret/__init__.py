from .... pyaz_utils import call_az

def add(certificate_store, certificate_url, cluster_name, resource_group, source_vault_id):
    '''
    Add a secret to the node type.
    '''
    return call_az("az sf managed-node-type vm-secret add", locals())

