from ..... pyaz_utils import call_az

def add(connection_monitor, endpoint_dest_name, endpoint_source_name, location, name, test_config_name, disable=None, endpoint_dest_address=None, endpoint_dest_resource_id=None, endpoint_source_address=None, endpoint_source_resource_id=None, frequency=None, http_method=None, http_path=None, http_port=None, http_valid_status_codes=None, https_prefer=None, icmp_disable_trace_route=None, preferred_ip_version=None, protocol=None, tcp_disable_trace_route=None, tcp_port=None, threshold_failed_percent=None, threshold_round_trip_time=None):
    '''
    Add a test group along with new-added/existing endpoint and test configuration to a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-group add", locals())


def remove(connection_monitor, location, name):
    '''
    Remove test group from a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-group remove", locals())


def show(connection_monitor, location, name):
    '''
    Show a test group of a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-group show", locals())


def list(connection_monitor, location):
    '''
    List all test groups of a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-group list", locals())

