from ... pyaz_utils import call_az

def create(cluster_name, name, resource_group, script_action_name, script_uri, access_mode=None, destination_port=None, disable_gateway_auth=None, edgenode_size=None, marketplace_id=None, no_validation_timeout=None, script_parameters=None, ssh_password=None, ssh_public_key=None, ssh_user=None, sub_domain_suffix=None, subnet=None, tags=None, type=None, vnet_name=None):
    '''
    Create an application for a HDInsight cluster.
    '''
    return call_az("az hdinsight application create", locals())


def show(cluster_name, name, resource_group):
    return call_az("az hdinsight application show", locals())


def list(cluster_name, resource_group):
    return call_az("az hdinsight application list", locals())


def wait(cluster_name, name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until an operation is complete.
    '''
    return call_az("az hdinsight application wait", locals())


def delete(cluster_name, name, resource_group, no_wait=None, yes=None):
    return call_az("az hdinsight application delete", locals())

