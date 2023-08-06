from .... pyaz_utils import _call_az

def add(cluster_name, resource_group, certificate_file=None, certificate_output_folder=None, certificate_password=None, certificate_subject_name=None, secret_identifier=None, vault_name=None, vault_rg=None):
    '''
    Add a new certificate to the Virtual Machine Scale Sets that make up the cluster to be used by hosted applications.
    '''
    return _call_az("az sf application certificate add", locals())

