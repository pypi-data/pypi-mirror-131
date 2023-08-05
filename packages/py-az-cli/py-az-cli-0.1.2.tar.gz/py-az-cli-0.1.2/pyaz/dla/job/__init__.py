from ... pyaz_utils import call_az
from . import pipeline, recurrence


def submit(account, job_name, script, compile_mode=None, compile_only=None, degree_of_parallelism=None, pipeline_id=None, pipeline_name=None, pipeline_uri=None, priority=None, recurrence_id=None, recurrence_name=None, run_id=None, runtime_version=None):
    '''
    Submit a job to a Data Lake Analytics account.
    '''
    return call_az("az dla job submit", locals())


def wait(account, job_id, max_wait_time_sec=None, wait_interval_sec=None):
    '''
    Wait for a Data Lake Analytics job to finish.
    '''
    return call_az("az dla job wait", locals())


def show(account, job_identity):
    '''
    Get information for a Data Lake Analytics job.
    '''
    return call_az("az dla job show", locals())


def cancel(account, job_identity):
    '''
    Cancel a Data Lake Analytics job.
    '''
    return call_az("az dla job cancel", locals())


def list(account, name=None, pipeline_id=None, recurrence_id=None, result=None, state=None, submitted_after=None, submitted_before=None, submitter=None, top=None):
    '''
    List Data Lake Analytics jobs.
    '''
    return call_az("az dla job list", locals())

