from .... pyaz_utils import call_az

def list(experiment, job, resource_group, workspace):
    '''
    List remote login information for nodes which executed the job.
    '''
    return call_az("az batchai job node list", locals())


def exec(experiment, job, resource_group, workspace, address=None, exec=None, node_id=None, password=None, ssh_private_key=None):
    '''
    Executes a command line on a cluster's node used to execute the job with optional ports forwarding.
    '''
    return call_az("az batchai job node exec", locals())

