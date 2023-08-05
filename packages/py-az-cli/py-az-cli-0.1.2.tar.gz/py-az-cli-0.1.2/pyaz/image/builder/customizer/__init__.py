from .... pyaz_utils import call_az

def add(customizer_name, name, resource_group, type, dest_path=None, exit_codes=None, file_source=None, filters=None, inline_script=None, restart_check_command=None, restart_command=None, restart_timeout=None, script_url=None, search_criteria=None, update_limit=None):
    '''
    Add an image builder customizer to an image builder template.
    '''
    return call_az("az image builder customizer add", locals())


def remove(customizer_name, name, resource_group):
    '''
    Remove an image builder customizer from an image builder template.
    '''
    return call_az("az image builder customizer remove", locals())


def clear(name, resource_group):
    '''
    Remove all image builder customizers from an image builder template.
    '''
    return call_az("az image builder customizer clear", locals())

