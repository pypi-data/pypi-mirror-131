from .... pyaz_utils import _call_az

def list(date_time_begin, date_time_end, granularity, metrics, profile_name, resource_group, actions=None, group_by=None, rule_types=None):
    return _call_az("az afd waf-log-analytic metric list", locals())

