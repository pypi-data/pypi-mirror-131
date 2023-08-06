from .... pyaz_utils import _call_az

def sync(name, resource_group):
    return _call_az("az batch account autostorage-keys sync", locals())

