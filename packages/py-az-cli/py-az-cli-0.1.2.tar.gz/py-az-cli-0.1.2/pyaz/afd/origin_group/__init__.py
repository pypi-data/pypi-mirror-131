from ... pyaz_utils import call_az

def show(origin_group_name, profile_name, resource_group):
    return call_az("az afd origin-group show", locals())


def list(profile_name, resource_group):
    return call_az("az afd origin-group list", locals())


def create(additional_latency_in_milliseconds, origin_group_name, probe_path, probe_protocol, probe_request_type, profile_name, resource_group, sample_size, successful_samples_required, probe_interval_in_seconds=None):
    '''
    Creates a new origin group within the specified profile.
    '''
    return call_az("az afd origin-group create", locals())


def update(origin_group_name, profile_name, resource_group, additional_latency_in_milliseconds=None, probe_interval_in_seconds=None, probe_path=None, probe_protocol=None, probe_request_type=None, sample_size=None, successful_samples_required=None):
    '''
    Creates a new origin group within the specified profile.
    '''
    return call_az("az afd origin-group update", locals())


def delete(origin_group_name, profile_name, resource_group, yes=None):
    '''
    Deletes an existing origin group within the specified profile.
    '''
    return call_az("az afd origin-group delete", locals())

