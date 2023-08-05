from ... pyaz_utils import call_az
from . import connection_monitor, flow_log, packet_capture, troubleshooting


def configure(locations, enabled=None, resource_group=None, tags=None):
    '''
    Configure the Network Watcher service for different regions.
    '''
    return call_az("az network watcher configure", locals())


def list():
    '''
    List Network Watchers.
    '''
    return call_az("az network watcher list", locals())


def test_ip_flow(direction, local, protocol, remote, vm, nic=None, resource_group=None):
    '''
    Test IP flow to/from a VM given the currently configured network security group rules.
    '''
    return call_az("az network watcher test-ip-flow", locals())


def test_connectivity(source_resource, dest_address=None, dest_port=None, dest_resource=None, headers=None, method=None, protocol=None, resource_group=None, source_port=None, valid_status_codes=None):
    '''
    Test if a connection can be established between a Virtual Machine and a given endpoint.
    '''
    return call_az("az network watcher test-connectivity", locals())


def show_next_hop(dest_ip, resource_group, source_ip, vm, nic=None):
    '''
    Get information on the 'next hop' of a VM.
    '''
    return call_az("az network watcher show-next-hop", locals())


def show_security_group_view(resource_group, vm):
    '''
    Get detailed security information on a VM for the currently configured network security group.
    '''
    return call_az("az network watcher show-security-group-view", locals())


def show_topology(location=None, resource_group=None, subnet=None, vnet=None):
    '''
    Get the network topology of a resource group, virtual network or subnet.
    '''
    return call_az("az network watcher show-topology", locals())


def run_configuration_diagnostic(resource, destination=None, direction=None, parent=None, port=None, protocol=None, queries=None, resource_group=None, resource_type=None, source=None):
    '''
    Run a configuration diagnostic on a target resource.
    '''
    return call_az("az network watcher run-configuration-diagnostic", locals())

