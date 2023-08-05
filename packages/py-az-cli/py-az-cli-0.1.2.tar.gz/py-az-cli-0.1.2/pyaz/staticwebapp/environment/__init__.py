from ... pyaz_utils import call_az

def list(name, resource_group=None):
    '''
    List all environment of the static app including production.
    '''
    return call_az("az staticwebapp environment list", locals())


def show(name, environment_name=None, resource_group=None):
    '''
    Show information about the production environment or the specified environment.
    '''
    return call_az("az staticwebapp environment show", locals())


def functions(name, environment_name=None, resource_group=None):
    '''
    Show information about functions.
    '''
    return call_az("az staticwebapp environment functions", locals())


def delete(name, environment_name=None, resource_group=None, yes=None):
    '''
    Delete the static app production environment or the specified environment.
    '''
    return call_az("az staticwebapp environment delete", locals())

