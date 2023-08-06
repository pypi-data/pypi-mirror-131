from ... pyaz_utils import _call_az

def show(name, resource_group):
    '''
    Get the status of Classic Azure Monitor logs integration on an HDInsight cluster.
    '''
    return _call_az("az hdinsight monitor show", locals())


def enable(name, resource_group, workspace, no_validation_timeout=None, primary_key=None):
    '''
    Enable the Classic Azure Monitor logs integration on an HDInsight cluster.
    '''
    return _call_az("az hdinsight monitor enable", locals())


def disable(name, resource_group):
    '''
    Disable the Classic Azure Monitor logs integration on an HDInsight cluster.
    '''
    return _call_az("az hdinsight monitor disable", locals())

