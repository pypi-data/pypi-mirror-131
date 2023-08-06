from ... pyaz_utils import _call_az

def list(resource_group, service_name):
    return _call_az("az search private-link-resource list", locals())

