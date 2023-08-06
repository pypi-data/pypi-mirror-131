from .... pyaz_utils import _call_az

def create(name, resource_group, workspace_name, compute_type=None, core_count=None, description=None, if_match=None, location=None, no_wait=None, time_to_live=None):
    '''
    Create an managed integration runtime.
    '''
    return _call_az("az synapse integration-runtime managed create", locals())

