from ... pyaz_utils import call_az

def create(account_endpoint=None, account_key=None, account_name=None, do_not_run_after=None, do_not_run_until=None, id=None, job_manager_task_command_line=None, job_manager_task_id=None, job_manager_task_resource_files=None, job_max_task_retry_count=None, job_max_wall_clock_time=None, json_file=None, max_parallel_tasks=None, metadata=None, on_all_tasks_complete=None, pool_id=None, priority=None, recurrence_interval=None, required_slots=None, start_window=None, uses_task_dependencies=None):
    '''
    Add a Batch job schedule to an account.
    '''
    return call_az("az batch job-schedule create", locals())


def delete(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, yes=None):
    return call_az("az batch job-schedule delete", locals())


def show(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, expand=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, select=None):
    return call_az("az batch job-schedule show", locals())


def set(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, do_not_run_after=None, do_not_run_until=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, job_manager_task_application_package_references=None, job_manager_task_command_line=None, job_manager_task_environment_settings=None, job_manager_task_id=None, job_manager_task_resource_files=None, job_metadata=None, json_file=None, max_parallel_tasks=None, metadata=None, on_all_tasks_complete=None, pool_id=None, priority=None, recurrence_interval=None, required_slots=None, start_window=None, uses_task_dependencies=None):
    '''
    Update the properties of a job schedule.
    '''
    return call_az("az batch job-schedule set", locals())


def reset(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, do_not_run_after=None, do_not_run_until=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, job_manager_task_application_package_references=None, job_manager_task_command_line=None, job_manager_task_environment_settings=None, job_manager_task_id=None, job_manager_task_resource_files=None, job_metadata=None, json_file=None, max_parallel_tasks=None, metadata=None, on_all_tasks_complete=None, pool_id=None, priority=None, recurrence_interval=None, required_slots=None, start_window=None, uses_task_dependencies=None):
    '''
    Reset the properties of a job schedule.  An updated job specification only applies to new jobs.
    '''
    return call_az("az batch job-schedule reset", locals())


def disable(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch job-schedule disable", locals())


def enable(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch job-schedule enable", locals())


def stop(job_schedule_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch job-schedule stop", locals())


def list(account_endpoint=None, account_key=None, account_name=None, expand=None, filter=None, select=None):
    return call_az("az batch job-schedule list", locals())

