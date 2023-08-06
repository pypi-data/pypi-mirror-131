from ..... pyaz_utils import _call_az

def create(aggregation, metric, operator, type, dimension=None, namespace=None, num_periods=None, num_violations=None, sensitivity=None, since=None, skip_metric_validation=None, threshold=None):
    '''
    Build a metric alert rule condition.
    '''
    return _call_az("az monitor metrics alert condition create", locals())

