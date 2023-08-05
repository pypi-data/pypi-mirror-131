from .... pyaz_utils import call_az

def create(database_options_json, name, project_name, resource_group, service_name, source_connection_json, target_connection_json, enable_data_integrity_validation=None, enable_query_analysis_validation=None, enable_schema_validation=None, task_type=None):
    '''
    Create and start a migration task.
    '''
    return call_az("az dms project task create", locals())


def cutover(name, object_name, project_name, resource_group, service_name):
    '''
    For an online migration task, complete the migration by performing a cutover.
    '''
    return call_az("az dms project task cutover", locals())


def delete(name, project_name, resource_group, service_name, delete_running_tasks=None, yes=None):
    '''
    Delete a migration task.
    '''
    return call_az("az dms project task delete", locals())


def list(project_name, resource_group, service_name, task_type=None):
    '''
    List the tasks within a project. Some tasks may have a status of Unknown, which indicates that an error occurred while querying the status of that task.
    '''
    return call_az("az dms project task list", locals())


def show(name, project_name, resource_group, service_name, expand=None):
    '''
    Show the details of a migration task. Use the "--expand" to get more details.
    '''
    return call_az("az dms project task show", locals())


def cancel(name, project_name, resource_group, service_name):
    '''
    Cancel a task if it's currently queued or running.
    '''
    return call_az("az dms project task cancel", locals())


def check_name(name, project_name, resource_group, service_name):
    '''
    Check if a given task name is available within a given instance of DMS as well as the name's validity.
    '''
    return call_az("az dms project task check-name", locals())

