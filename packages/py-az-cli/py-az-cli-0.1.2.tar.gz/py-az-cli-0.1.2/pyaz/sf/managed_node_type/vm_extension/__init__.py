from .... pyaz_utils import call_az

def add(cluster_name, extension_name, extension_type, publisher, resource_group, type_handler_version, auto_upgrade_minor_version=None, force_update_tag=None, protected_setting=None, provision_after_extension=None, setting=None):
    '''
    Add an extension to the node type.
    '''
    return call_az("az sf managed-node-type vm-extension add", locals())


def delete(cluster_name, extension_name, resource_group):
    '''
    Delete an extension to the node type.
    '''
    return call_az("az sf managed-node-type vm-extension delete", locals())

