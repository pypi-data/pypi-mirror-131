from .... pyaz_utils import call_az

def disable(pool_id, account_endpoint=None, account_key=None, account_name=None):
    return call_az("az batch pool autoscale disable", locals())


def enable(pool_id, account_endpoint=None, account_key=None, account_name=None, auto_scale_evaluation_interval=None, auto_scale_formula=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch pool autoscale enable", locals())


def evaluate(auto_scale_formula, pool_id, account_endpoint=None, account_key=None, account_name=None):
    return call_az("az batch pool autoscale evaluate", locals())

