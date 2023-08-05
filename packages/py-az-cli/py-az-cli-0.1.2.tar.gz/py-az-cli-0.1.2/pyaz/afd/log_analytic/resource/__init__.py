from .... pyaz_utils import call_az

def list(profile_name, resource_group):
    return call_az("az afd log-analytic resource list", locals())

