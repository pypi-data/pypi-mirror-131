from ... pyaz_utils import call_az

def show(name, resource_group):
    '''
    Get the status of Azure Monitor logs integration on an HDInsight cluster.
    '''
    return call_az("az hdinsight azure-monitor show", locals())


def enable(name, resource_group, workspace, no_validation_timeout=None, primary_key=None):
    '''
    Enable the Azure Monitor logs integration on an HDInsight cluster.
    '''
    return call_az("az hdinsight azure-monitor enable", locals())


def disable(name, resource_group):
    '''
    Disable the Azure Monitor logs integration on an HDInsight cluster.
    '''
    return call_az("az hdinsight azure-monitor disable", locals())

