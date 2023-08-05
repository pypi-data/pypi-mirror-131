from .. pyaz_utils import call_az
from . import db, dw, elastic_pool, failover_group, instance_failover_group, instance_pool, midb, stg, virtual_cluster, vm


def list_usages(location):
    return call_az("az sql list-usages", locals())


def show_usage(location, usage):
    return call_az("az sql show-usage", locals())

