from ..... pyaz_utils import call_az

def add(connection_monitor, location, name, protocol, test_groups, frequency=None, http_method=None, http_path=None, http_port=None, http_prefer_https=None, http_request_header=None, http_valid_status_codes=None, icmp_disable_trace_route=None, preferred_ip_version=None, tcp_disable_trace_route=None, tcp_port=None, tcp_port_behavior=None, threshold_failed_percent=None, threshold_round_trip_time=None):
    '''
    Add a test configuration to a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-configuration add", locals())


def remove(connection_monitor, location, name, test_groups=None):
    '''
    Remove a test configuration from a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-configuration remove", locals())


def show(connection_monitor, location, name):
    '''
    Show a test configuration from a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-configuration show", locals())


def list(connection_monitor, location):
    '''
    List all test configurations of a connection monitor
    '''
    return call_az("az network watcher connection-monitor test-configuration list", locals())

