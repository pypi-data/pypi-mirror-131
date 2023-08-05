from .... pyaz_utils import call_az

def tail(name, resource_group, aggregation=None, dimension=None, end_time=None, filter=None, interval=None, metadata=None, metrics=None, namespace=None, offset=None, orderby=None, start_time=None, top=None):
    '''
    List the metric values for a VM.
    '''
    return call_az("az vm monitor metrics tail", locals())


def list_definitions(name, resource_group, namespace=None):
    '''
    List the metric definitions for a VM.
    '''
    return call_az("az vm monitor metrics list-definitions", locals())

