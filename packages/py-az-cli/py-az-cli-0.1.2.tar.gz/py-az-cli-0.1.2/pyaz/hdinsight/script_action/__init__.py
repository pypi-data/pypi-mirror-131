from ... pyaz_utils import call_az

def show_execution_details(cluster_name, execution_id, resource_group):
    return call_az("az hdinsight script-action show-execution-details", locals())


def list(cluster_name, resource_group):
    return call_az("az hdinsight script-action list", locals())


def delete(cluster_name, name, resource_group):
    return call_az("az hdinsight script-action delete", locals())


def execute(cluster_name, name, resource_group, roles, script_uri, persist_on_success=None, script_parameters=None):
    '''
    Execute script actions on the specified HDInsight cluster.
    '''
    return call_az("az hdinsight script-action execute", locals())


def list_execution_history(cluster_name, resource_group):
    return call_az("az hdinsight script-action list-execution-history", locals())


def promote(cluster_name, execution_id, resource_group):
    return call_az("az hdinsight script-action promote", locals())

