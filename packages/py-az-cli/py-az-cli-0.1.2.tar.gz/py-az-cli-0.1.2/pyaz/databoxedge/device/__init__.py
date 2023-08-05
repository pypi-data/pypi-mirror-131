from ... pyaz_utils import call_az

def list(expand=None, resource_group=None):
    '''
    Get all the Data Box Edge/Data Box Gateway devices in a resource group or in a subscription.
    '''
    return call_az("az databoxedge device list", locals())


def show(name, resource_group):
    '''
    Get the properties of the Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge device show", locals())


def create(name, resource_group, description=None, etag=None, friendly_name=None, location=None, model_description=None, no_wait=None, sku=None, status=None, tags=None):
    '''
    Create a Data Box Edge/Data Box Gateway resource.
    '''
    return call_az("az databoxedge device create", locals())


def update(name, resource_group, tags=None):
    '''
    Modify a Data Box Edge/Data Box Gateway resource.
    '''
    return call_az("az databoxedge device update", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete the Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge device delete", locals())


def download_update(name, resource_group, no_wait=None):
    '''
    Download the updates on a Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge device download-update", locals())


def install_update(name, resource_group, no_wait=None):
    '''
    Install the updates on the Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge device install-update", locals())


def scan_for_update(name, resource_group, no_wait=None):
    '''
    Scan for updates on a Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge device scan-for-update", locals())


def show_update_summary(name, resource_group):
    '''
    Get information about the availability of updates based on the last scan of the device. It also gets information about any ongoing download or install jobs on the device.
    '''
    return call_az("az databoxedge device show-update-summary", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the databoxedge device is met.
    '''
    return call_az("az databoxedge device wait", locals())

