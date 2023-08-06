from .. pyaz_utils import _call_az

def list(resource_group=None):
    '''
    List all deployment scripts.
    '''
    return _call_az("az deployment-scripts list", locals())


def show(name, resource_group):
    '''
    Retrieve a deployment script.
    '''
    return _call_az("az deployment-scripts show", locals())


def show_log(name, resource_group):
    '''
    Show deployment script logs.
    '''
    return _call_az("az deployment-scripts show-log", locals())


def delete(name, resource_group, yes=None):
    '''
    Delete a deployment script.
    '''
    return _call_az("az deployment-scripts delete", locals())

