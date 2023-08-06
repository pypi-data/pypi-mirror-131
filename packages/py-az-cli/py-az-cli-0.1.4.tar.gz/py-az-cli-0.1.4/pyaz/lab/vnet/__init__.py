from ... pyaz_utils import _call_az

def list(lab_name, resource_group, expand=None, filter=None, orderby=None, top=None):
    return _call_az("az lab vnet list", locals())


def get(lab_name, name, resource_group, expand=None):
    return _call_az("az lab vnet get", locals())

