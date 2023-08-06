from ... pyaz_utils import _call_az

def show(resource_group, service_name):
    return _call_az("az search admin-key show", locals())


def renew(key_kind, resource_group, service_name):
    return _call_az("az search admin-key renew", locals())

