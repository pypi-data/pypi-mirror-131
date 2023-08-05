from ... pyaz_utils import call_az

def create(resource_group, duration=None, location=None, step=None, step_name=None, tags=None):
    '''
    Creates the step.
    '''
    return call_az("az deploymentmanager step create", locals())


def delete(resource_group, step_name):
    return call_az("az deploymentmanager step delete", locals())


def show(resource_group, step_name):
    '''
    Get the details of the step.
    '''
    return call_az("az deploymentmanager step show", locals())


def list(resource_group):
    '''
    List all steps in a resource group.
    '''
    return call_az("az deploymentmanager step list", locals())


def update(resource_group, step_name, add=None, duration=None, force_string=None, remove=None, set=None, step=None, tags=None):
    '''
    Updates the step.
    '''
    return call_az("az deploymentmanager step update", locals())

