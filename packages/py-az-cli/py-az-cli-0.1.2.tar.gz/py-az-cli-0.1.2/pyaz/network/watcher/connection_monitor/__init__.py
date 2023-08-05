from .... pyaz_utils import call_az
from . import endpoint, output, test_configuration, test_group


def create(name, dest_address=None, dest_port=None, dest_resource=None, do_not_start=None, endpoint_dest_address=None, endpoint_dest_coverage_level=None, endpoint_dest_name=None, endpoint_dest_resource_id=None, endpoint_dest_type=None, endpoint_source_address=None, endpoint_source_coverage_level=None, endpoint_source_name=None, endpoint_source_resource_id=None, endpoint_source_type=None, frequency=None, http_method=None, http_path=None, http_port=None, http_valid_status_codes=None, https_prefer=None, icmp_disable_trace_route=None, location=None, monitoring_interval=None, notes=None, output_type=None, preferred_ip_version=None, protocol=None, resource_group=None, source_port=None, source_resource=None, tags=None, tcp_disable_trace_route=None, tcp_port=None, tcp_port_behavior=None, test_config_name=None, test_group_disable=None, test_group_name=None, threshold_failed_percent=None, threshold_round_trip_time=None, workspace_ids=None):
    '''
    Create a connection monitor.
    '''
    return call_az("az network watcher connection-monitor create", locals())


def delete(location, name, resource_group=None):
    '''
    Delete a connection monitor for the given region.
    '''
    return call_az("az network watcher connection-monitor delete", locals())


def show(location, name, resource_group=None):
    '''
    Shows a connection monitor by name.
    '''
    return call_az("az network watcher connection-monitor show", locals())


def stop(location, name, resource_group=None):
    '''
    Stop the specified connection monitor.
    '''
    return call_az("az network watcher connection-monitor stop", locals())


def start(location, name, resource_group=None):
    '''
    Start the specified connection monitor.
    '''
    return call_az("az network watcher connection-monitor start", locals())


def query(location, name, resource_group=None):
    '''
    Query a snapshot of the most recent connection state of a connection monitor.
    '''
    return call_az("az network watcher connection-monitor query", locals())


def list(location, resource_group=None):
    '''
    List connection monitors for the given region.
    '''
    return call_az("az network watcher connection-monitor list", locals())

