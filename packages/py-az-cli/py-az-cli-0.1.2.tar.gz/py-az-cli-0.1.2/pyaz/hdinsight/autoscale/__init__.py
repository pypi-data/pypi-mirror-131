from ... pyaz_utils import call_az
from . import condition


def create(cluster_name, resource_group, type, days=None, max_workernode_count=None, min_workernode_count=None, no_wait=None, time=None, timezone=None, workernode_count=None, yes=None):
    '''
    Enable Autoscale for a running cluster.
    '''
    return call_az("az hdinsight autoscale create", locals())


def update(cluster_name, resource_group, max_workernode_count=None, min_workernode_count=None, no_wait=None, timezone=None):
    '''
    Update the Autoscale configuration.
    '''
    return call_az("az hdinsight autoscale update", locals())


def show(cluster_name, resource_group):
    '''
    Get the Autoscale configuration of a specified cluster.
    '''
    return call_az("az hdinsight autoscale show", locals())


def delete(cluster_name, resource_group, no_wait=None, yes=None):
    '''
    Disable Autoscale for a running cluster.
    '''
    return call_az("az hdinsight autoscale delete", locals())


def list_timezones():
    '''
    List the available timezone name when enabling Schedule-based Autoscale.
    '''
    return call_az("az hdinsight autoscale list-timezones", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until an operation is complete.
    '''
    return call_az("az hdinsight autoscale wait", locals())

