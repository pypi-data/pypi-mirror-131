from ... pyaz_utils import call_az

def create(name, parameters, resource_group):
    return call_az("az monitor autoscale-settings create", locals())


def delete(name, resource_group):
    return call_az("az monitor autoscale-settings delete", locals())


def show(name, resource_group):
    return call_az("az monitor autoscale-settings show", locals())


def list(resource_group):
    return call_az("az monitor autoscale-settings list", locals())


def get_parameters_template():
    return call_az("az monitor autoscale-settings get-parameters-template", locals())


def update(name, resource_group, add=None, force_string=None, remove=None, set=None):
    '''
    Updates an autoscale setting.
    '''
    return call_az("az monitor autoscale-settings update", locals())

