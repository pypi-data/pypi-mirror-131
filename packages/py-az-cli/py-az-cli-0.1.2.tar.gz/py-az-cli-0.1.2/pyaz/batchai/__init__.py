from .. pyaz_utils import call_az
from . import cluster, experiment, file_server, job, workspace


def list_usages(location):
    '''
    Gets the current usage information as well as limits for Batch AI resources for given location.
    '''
    return call_az("az batchai list-usages", locals())

