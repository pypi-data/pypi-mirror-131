from ... pyaz_utils import call_az

def browse(name, resource_group, disable_browser=None, ssh_key_file=None):
    return call_az("az acs kubernetes browse", locals())


def get_credentials(name, resource_group, file=None, overwrite_existing=None, ssh_key_file=None):
    '''
    Download and install credentials to access a cluster.  This command requires the same private-key used to create the cluster.
    '''
    return call_az("az acs kubernetes get-credentials", locals())


def install_cli(base_src_url=None, client_version=None, install_location=None, kubelogin_base_src_url=None, kubelogin_install_location=None, kubelogin_version=None):
    '''
    Download and install the Kubernetes command-line tool for a cluster.
    '''
    return call_az("az acs kubernetes install-cli", locals())

