from ... pyaz_utils import _call_az

def list(resource_group=None):
    '''
    List security tasks (recommendations).
    '''
    return _call_az("az security task list", locals())


def show(name, resource_group=None):
    '''
    shows a security task (recommendation).
    '''
    return _call_az("az security task show", locals())

