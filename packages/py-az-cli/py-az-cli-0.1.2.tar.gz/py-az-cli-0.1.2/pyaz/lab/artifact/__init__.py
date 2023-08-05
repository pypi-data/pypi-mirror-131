from ... pyaz_utils import call_az

def list(artifact_source_name, lab_name, resource_group, expand=None, filter=None, orderby=None, top=None):
    return call_az("az lab artifact list", locals())

