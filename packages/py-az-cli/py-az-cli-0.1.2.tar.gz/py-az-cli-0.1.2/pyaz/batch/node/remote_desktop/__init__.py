from .... pyaz_utils import call_az

def download(destination, node_id, pool_id, account_endpoint=None, account_key=None, account_name=None):
    return call_az("az batch node remote-desktop download", locals())

