from .... pyaz_utils import call_az

def delete(id=None, name=None, namespace_name=None, resource_group=None, yes=None):
    '''
    Delete a private endpoint connection request for eventhubs namespace.
    '''
    return call_az("az eventhubs namespace private-endpoint-connection delete", locals())


def show(id=None, name=None, namespace_name=None, resource_group=None):
    '''
    Show details of a private endpoint connection request for eventhubs namespace.
    '''
    return call_az("az eventhubs namespace private-endpoint-connection show", locals())


def list(namespace_name, resource_group):
    return call_az("az eventhubs namespace private-endpoint-connection list", locals())


def approve(description=None, id=None, name=None, namespace_name=None, resource_group=None):
    '''
    Approve a private endpoint connection request for eventhubs namesapce.
    '''
    return call_az("az eventhubs namespace private-endpoint-connection approve", locals())


def reject(description=None, id=None, name=None, namespace_name=None, resource_group=None):
    '''
    Reject a private endpoint connection request for eventhubs namespace.
    '''
    return call_az("az eventhubs namespace private-endpoint-connection reject", locals())

