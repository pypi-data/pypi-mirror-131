from .... pyaz_utils import _call_az

def disable(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, node_disable_scheduling_option=None):
    return _call_az("az batch node scheduling disable", locals())


def enable(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None):
    return _call_az("az batch node scheduling enable", locals())

