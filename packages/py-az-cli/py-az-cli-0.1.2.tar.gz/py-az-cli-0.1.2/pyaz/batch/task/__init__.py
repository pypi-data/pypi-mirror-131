from ... pyaz_utils import call_az
from . import file, subtask


def create(job_id, account_endpoint=None, account_key=None, account_name=None, affinity_id=None, application_package_references=None, command_line=None, environment_settings=None, json_file=None, max_task_retry_count=None, max_wall_clock_time=None, resource_files=None, retention_time=None, task_id=None):
    '''
    Create Batch tasks.
    '''
    return call_az("az batch task create", locals())


def list(job_id, account_endpoint=None, account_key=None, account_name=None, expand=None, filter=None, select=None):
    return call_az("az batch task list", locals())


def delete(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, yes=None):
    return call_az("az batch task delete", locals())


def show(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, expand=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, select=None):
    return call_az("az batch task show", locals())


def reset(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, json_file=None, max_task_retry_count=None, max_wall_clock_time=None, retention_time=None):
    '''
    Reset the properties of a Batch task.
    '''
    return call_az("az batch task reset", locals())


def reactivate(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch task reactivate", locals())


def stop(job_id, task_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None):
    return call_az("az batch task stop", locals())

