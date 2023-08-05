from ... pyaz_utils import call_az

def create(name, resource_group, workspace):
    '''
    Create an experiment.
    '''
    return call_az("az batchai experiment create", locals())


def show(name, resource_group, workspace):
    '''
    Show information about an experiment.
    '''
    return call_az("az batchai experiment show", locals())


def list(resource_group, workspace):
    '''
    List experiments.
    '''
    return call_az("az batchai experiment list", locals())


def delete(name, resource_group, workspace, no_wait=None, yes=None):
    '''
    Delete an experiment.
    '''
    return call_az("az batchai experiment delete", locals())

