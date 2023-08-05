from ... pyaz_utils import call_az

def invoke(command_id, name, resource_group, parameters=None, scripts=None):
    '''
    Execute a specific run command on a vm.
    '''
    return call_az("az vm run-command invoke", locals())


def list(expand=None, location=None, resource_group=None, vm_name=None):
    '''
    The operation to get all run commands of a Virtual Machine. And Lists all available run commands for a subscription in a location.
    '''
    return call_az("az vm run-command list", locals())


def show(command_id=None, expand=None, instance_view=None, location=None, name=None, resource_group=None, vm_name=None):
    '''
    The operation to get the run command. And Gets specific run command for a subscription in a location.
    '''
    return call_az("az vm run-command show", locals())


def create(name, resource_group, vm_name, async_execution=None, command_id=None, error_blob_uri=None, location=None, no_wait=None, output_blob_uri=None, parameters=None, protected_parameters=None, run_as_password=None, run_as_user=None, script=None, script_uri=None, tags=None, timeout_in_seconds=None):
    '''
    The operation to create the run command.
    '''
    return call_az("az vm run-command create", locals())


def update(name, resource_group, vm_name, async_execution=None, command_id=None, error_blob_uri=None, location=None, no_wait=None, output_blob_uri=None, parameters=None, protected_parameters=None, run_as_password=None, run_as_user=None, script=None, script_uri=None, tags=None, timeout_in_seconds=None):
    '''
    The operation to update the run command.
    '''
    return call_az("az vm run-command update", locals())


def delete(name, resource_group, vm_name, no_wait=None, yes=None):
    '''
    The operation to delete the run command.
    '''
    return call_az("az vm run-command delete", locals())


def wait(command_id=None, created=None, custom=None, deleted=None, exists=None, expand=None, instance_view=None, interval=None, location=None, name=None, resource_group=None, timeout=None, updated=None, vm_name=None):
    '''
    Place the CLI in a waiting state until a condition of the res virtual-machine-run-command is met.
    '''
    return call_az("az vm run-command wait", locals())

