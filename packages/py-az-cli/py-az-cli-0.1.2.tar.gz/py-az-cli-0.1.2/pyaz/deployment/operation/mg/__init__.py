from .... pyaz_utils import call_az

def list(management_group_id, name):
    '''
    List deployment operations at management group.
    '''
    return call_az("az deployment operation mg list", locals())


def show(management_group_id, name, operation_ids):
    '''
    Show a deployment operation at management group.
    '''
    return call_az("az deployment operation mg show", locals())

