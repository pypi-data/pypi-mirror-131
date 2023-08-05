from .... pyaz_utils import call_az

def upload(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, container_url=None, end_time=None, json_file=None, resource_id=None, start_time=None):
    return call_az("az batch node service-logs upload", locals())

