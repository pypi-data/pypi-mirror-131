from .... pyaz_utils import call_az

def set(cluster_name, resource_group, parameter=None, section=None, settings_section_description=None, value=None):
    '''
    Update the settings of a cluster.
    '''
    return call_az("az sf cluster setting set", locals())


def remove(cluster_name, resource_group, parameter=None, section=None, settings_section_description=None):
    '''
    Remove settings from a cluster.
    '''
    return call_az("az sf cluster setting remove", locals())

