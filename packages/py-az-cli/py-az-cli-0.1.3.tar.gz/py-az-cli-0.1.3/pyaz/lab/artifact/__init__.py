from ... pyaz_utils import _call_az

def list(artifact_source_name, lab_name, resource_group, expand=None, filter=None, orderby=None, top=None):
    return _call_az("az lab artifact list", locals())

