from ... pyaz_utils import call_az

def show(name, node_name, resource_group, workspace_name):
    '''
    Get self-hosted integration runtime node information.
    '''
    return call_az("az synapse integration-runtime-node show", locals())


def update(auto_update, name, node_name, resource_group, update_delay_offset, workspace_name):
    '''
    Update self-hosted integration runtime node.
    '''
    return call_az("az synapse integration-runtime-node update", locals())


def delete(name, node_name, resource_group, workspace_name, yes=None):
    '''
    Remove a self-hosted integration runtime node.
    '''
    return call_az("az synapse integration-runtime-node delete", locals())


def get_ip_address(name, node_name, resource_group, workspace_name):
    '''
    Get self-hosted integration runtime node ip.
    '''
    return call_az("az synapse integration-runtime-node get-ip-address", locals())

