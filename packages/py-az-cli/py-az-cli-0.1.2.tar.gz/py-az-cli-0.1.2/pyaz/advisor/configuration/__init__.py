from ... pyaz_utils import call_az

def list():
    '''
    List Azure Advisor configuration for the entire subscription.
    '''
    return call_az("az advisor configuration list", locals())


def show(resource_group=None):
    '''
    Show Azure Advisor configuration for the given subscription or resource group.
    '''
    return call_az("az advisor configuration show", locals())


def update(add=None, configuration_name=None, exclude=None, force_string=None, include=None, low_cpu_threshold=None, remove=None, resource_group=None, set=None):
    '''
    Update Azure Advisor configuration.
    '''
    return call_az("az advisor configuration update", locals())

