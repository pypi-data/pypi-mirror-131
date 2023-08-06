from .... pyaz_utils import _call_az

def list(custom_domains, date_time_begin, date_time_end, granularity, metrics, profile_name, protocols, resource_group, continents=None, country_or_regions=None, group_by=None):
    return _call_az("az afd log-analytic metric list", locals())

