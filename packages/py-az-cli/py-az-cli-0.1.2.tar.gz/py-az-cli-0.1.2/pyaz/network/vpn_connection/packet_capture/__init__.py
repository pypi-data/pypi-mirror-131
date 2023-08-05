from .... pyaz_utils import call_az

def start(name, resource_group, filter=None, no_wait=None):
    '''
    Start packet capture on a VPN connection.
    '''
    return call_az("az network vpn-connection packet-capture start", locals())


def stop(name, resource_group, sas_url, no_wait=None):
    '''
    Stop packet capture on a VPN connection.
    '''
    return call_az("az network vpn-connection packet-capture stop", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the vpn connection packet capture is met.
    '''
    return call_az("az network vpn-connection packet-capture wait", locals())

