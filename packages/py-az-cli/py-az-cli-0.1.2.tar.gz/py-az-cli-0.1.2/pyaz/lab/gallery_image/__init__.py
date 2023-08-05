from ... pyaz_utils import call_az

def list(lab_name, resource_group, expand=None, filter=None, orderby=None, top=None):
    return call_az("az lab gallery-image list", locals())

