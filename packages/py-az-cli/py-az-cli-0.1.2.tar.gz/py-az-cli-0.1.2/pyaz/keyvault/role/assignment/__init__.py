from .... pyaz_utils import call_az

def delete(assignee=None, assignee_object_id=None, hsm_name=None, id=None, ids=None, name=None, role=None, scope=None):
    return call_az("az keyvault role assignment delete", locals())


def list(assignee=None, assignee_object_id=None, hsm_name=None, id=None, role=None, scope=None):
    return call_az("az keyvault role assignment list", locals())


def create(role, scope, assignee=None, assignee_object_id=None, assignee_principal_type=None, hsm_name=None, id=None, name=None):
    return call_az("az keyvault role assignment create", locals())

