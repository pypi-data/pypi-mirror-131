from ... pyaz_utils import _call_az

def set(lab_name, name, resource_group, value):
    '''
    Set a secret for a lab.
    '''
    return _call_az("az lab secret set", locals())


def show(lab_name, name, resource_group, expand=None):
    return _call_az("az lab secret show", locals())


def list(lab_name, resource_group, expand=None, filter=None, orderby=None, top=None):
    return _call_az("az lab secret list", locals())


def delete(lab_name, name, resource_group):
    return _call_az("az lab secret delete", locals())

