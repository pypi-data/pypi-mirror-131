from ... pyaz_utils import call_az

def show(account_name, name, resource_group, transform_name):
    '''
    Show the details of a job.
    '''
    return call_az("az ams job show", locals())


def list(account_name, resource_group, transform_name, filter=None, orderby=None):
    '''
    List all the jobs of a transform within an Azure Media Services account.
    '''
    return call_az("az ams job list", locals())


def delete(account_name, name, resource_group, transform_name):
    '''
    Delete a job.
    '''
    return call_az("az ams job delete", locals())


def cancel(account_name, name, resource_group, transform_name, delete=None):
    '''
    Cancel a job.
    '''
    return call_az("az ams job cancel", locals())


def start(account_name, name, output_assets, resource_group, transform_name, base_uri=None, correlation_data=None, description=None, files=None, input_asset_name=None, label=None, priority=None):
    '''
    Start a job.
    '''
    return call_az("az ams job start", locals())


def update(account_name, name, resource_group, transform_name, add=None, description=None, force_string=None, priority=None, remove=None, set=None):
    '''
    Update an existing job.
    '''
    return call_az("az ams job update", locals())

