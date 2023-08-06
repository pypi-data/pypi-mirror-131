from .... pyaz_utils import _call_az

def list(profile_name, resource_group):
    return _call_az("az afd log-analytic location list", locals())

