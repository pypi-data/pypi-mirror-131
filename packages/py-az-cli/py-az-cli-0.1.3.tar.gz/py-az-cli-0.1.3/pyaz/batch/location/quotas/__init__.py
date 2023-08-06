from .... pyaz_utils import _call_az

def show(location):
    return _call_az("az batch location quotas show", locals())

