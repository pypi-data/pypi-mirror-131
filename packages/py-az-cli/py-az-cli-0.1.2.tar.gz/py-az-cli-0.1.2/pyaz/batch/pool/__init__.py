from ... pyaz_utils import call_az
from . import all_statistics, autoscale, node_counts, supported_images, usage_metrics


def create(account_endpoint=None, account_key=None, account_name=None, application_licenses=None, application_package_references=None, auto_scale_formula=None, certificate_references=None, disk_encryption_targets=None, enable_inter_node_communication=None, id=None, image=None, json_file=None, metadata=None, node_agent_sku_id=None, offer=None, os_family=None, os_version=None, policy=None, publisher=None, resize_timeout=None, sku=None, start_task_command_line=None, start_task_resource_files=None, start_task_wait_for_success=None, target_dedicated_nodes=None, target_low_priority_nodes=None, targets=None, task_slots_per_node=None, version=None, virtual_machine_image_id=None, vm_size=None):
    '''
    Create a Batch pool in an account. When creating a pool, choose arguments from either Cloud Services Configuration or Virtual Machine Configuration.
    '''
    return call_az("az batch pool create", locals())


def list(account_endpoint=None, account_key=None, account_name=None, expand=None, filter=None, select=None):
    return call_az("az batch pool list", locals())


def delete(pool_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, yes=None):
    return call_az("az batch pool delete", locals())


def show(pool_id, account_endpoint=None, account_key=None, account_name=None, expand=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, select=None):
    return call_az("az batch pool show", locals())


def set(pool_id, account_endpoint=None, account_key=None, account_name=None, application_package_references=None, certificate_references=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, json_file=None, metadata=None, start_task_command_line=None, start_task_environment_settings=None, start_task_max_task_retry_count=None, start_task_resource_files=None, start_task_wait_for_success=None):
    '''
    Update the properties of a Batch pool. Updating a property in a subgroup will reset the unspecified properties of that group.
    '''
    return call_az("az batch pool set", locals())


def reset(pool_id, account_endpoint=None, account_key=None, account_name=None, application_package_references=None, certificate_references=None, json_file=None, metadata=None, start_task_command_line=None, start_task_environment_settings=None, start_task_max_task_retry_count=None, start_task_wait_for_success=None):
    '''
    Update the properties of a Batch pool. Unspecified properties which can be updated are reset to their defaults.
    '''
    return call_az("az batch pool reset", locals())


def resize(pool_id, abort=None, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, node_deallocation_option=None, resize_timeout=None, target_dedicated_nodes=None, target_low_priority_nodes=None):
    '''
    Resize or stop resizing a Batch pool.
    '''
    return call_az("az batch pool resize", locals())

