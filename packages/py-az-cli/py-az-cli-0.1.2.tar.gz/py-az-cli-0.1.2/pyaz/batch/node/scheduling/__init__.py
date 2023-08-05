from .... pyaz_utils import call_az

def disable(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, node_disable_scheduling_option=None):
    return call_az("az batch node scheduling disable", locals())


def enable(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None):
    return call_az("az batch node scheduling enable", locals())

