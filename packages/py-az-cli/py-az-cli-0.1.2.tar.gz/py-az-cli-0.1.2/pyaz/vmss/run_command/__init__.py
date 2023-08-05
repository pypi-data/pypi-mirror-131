from ... pyaz_utils import call_az

def invoke(command_id, instance_id, name, resource_group, parameters=None, scripts=None):
    '''
    Execute a specific run command on a Virtual Machine Scale Set instance.
    '''
    return call_az("az vmss run-command invoke", locals())


def list(instance_id, resource_group, vmss_name, expand=None):
    '''
    The operation to get all run commands of an instance in Virtual Machine Scaleset.
    '''
    return call_az("az vmss run-command list", locals())


def show(instance_id, name, resource_group, vmss_name, expand=None, instance_view=None):
    '''
    The operation to get the VMSS run command.
    '''
    return call_az("az vmss run-command show", locals())


def create(instance_id, name, resource_group, vmss_name, async_execution=None, command_id=None, error_blob_uri=None, location=None, no_wait=None, output_blob_uri=None, parameters=None, protected_parameters=None, run_as_password=None, run_as_user=None, script=None, script_uri=None, tags=None, timeout_in_seconds=None):
    '''
    The operation to Create the VMSS VM run command.
    '''
    return call_az("az vmss run-command create", locals())


def update(instance_id, name, resource_group, vmss_name, async_execution=None, command_id=None, error_blob_uri=None, location=None, no_wait=None, output_blob_uri=None, parameters=None, protected_parameters=None, run_as_password=None, run_as_user=None, script=None, script_uri=None, tags=None, timeout_in_seconds=None):
    '''
    The operation to update the VMSS run command.
    '''
    return call_az("az vmss run-command update", locals())


def delete(instance_id, name, resource_group, vmss_name, no_wait=None, yes=None):
    '''
    The operation to delete the run command.
    '''
    return call_az("az vmss run-command delete", locals())

