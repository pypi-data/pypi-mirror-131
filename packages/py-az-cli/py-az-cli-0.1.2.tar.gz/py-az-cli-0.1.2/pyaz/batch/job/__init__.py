from ... pyaz_utils import call_az
from . import all_statistics, prep_release_status, task_counts


def create(account_endpoint=None, account_key=None, account_name=None, id=None, job_manager_task_command_line=None, job_manager_task_environment_settings=None, job_manager_task_id=None, job_manager_task_resource_files=None, job_max_task_retry_count=None, job_max_wall_clock_time=None, json_file=None, max_parallel_tasks=None, metadata=None, pool_id=None, priority=None, required_slots=None, uses_task_dependencies=None):
    '''
    Add a job to a Batch account.
    '''
    return call_az("az batch job create", locals())


def delete(job_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, yes=None):
    return call_az("az batch job delete", locals())


def show(job_id, account_endpoint=None, account_key=None, account_name=None, expand=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, select=None):
    return call_az("az batch job show", locals())


def set(job_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, job_max_task_retry_count=None, job_max_wall_clock_time=None, json_file=None, max_parallel_tasks=None, metadata=None, on_all_tasks_complete=None, pool_id=None, priority=None):
    '''
    Update the properties of a Batch job. Updating a property in a subgroup will reset the unspecified properties of that group.
    '''
    return call_az("az batch job set", locals())


def reset(job_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, job_max_task_retry_count=None, job_max_wall_clock_time=None, json_file=None, metadata=None, on_all_tasks_complete=None, pool_id=None, priority=None):
    '''
    Update the properties of a Batch job. Unspecified properties which can be updated are reset to their defaults.
    '''
    return call_az("az batch job reset", locals())


def list(account_endpoint=None, account_key=None, account_name=None, expand=None, filter=None, job_schedule_id=None, select=None):
    '''
    List all of the jobs or job schedule in a Batch account.
    '''
    return call_az("az batch job list", locals())


def disable(job_id, account_endpoint=None, account_key=None, account_name=None, disable_tasks=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch job disable", locals())


def enable(job_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch job enable", locals())


def stop(job_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, terminate_reason=None):
    '''
    Stop a running Batch job.
    '''
    return call_az("az batch job stop", locals())

