from .... pyaz_utils import call_az

def show(location):
    return call_az("az batch location quotas show", locals())

