from .. pyaz_utils import call_az
from . import appsettings, environment, functions, hostname, identity, secrets, users


def list(resource_group=None):
    '''
    List all static app resources in a subscription, or in resource group if provided
    '''
    return call_az("az staticwebapp list", locals())


def show(name, resource_group=None):
    '''
    Show details of a static app.
    '''
    return call_az("az staticwebapp show", locals())


def create(branch, location, name, resource_group, source, api_location=None, app_location=None, login_with_github=None, no_wait=None, output_location=None, sku=None, tags=None, token=None):
    '''
    Create a static app with content from a GitHub repository URL and on the provided branch. If the repo is under a Github organization, please ensure that the Azure CLI Github App has access to the organization. Access can be requested in the browser when using the "--login-with-github" argument. Access must be granted by the organization's admin.
    '''
    return call_az("az staticwebapp create", locals())


def delete(name, no_wait=None, resource_group=None, yes=None):
    '''
    Delete a static app.
    '''
    return call_az("az staticwebapp delete", locals())


def disconnect(name, no_wait=None, resource_group=None):
    '''
    Disconnect source control to enable connecting to a different repo.
    '''
    return call_az("az staticwebapp disconnect", locals())


def reconnect(branch, name, source, login_with_github=None, no_wait=None, resource_group=None, token=None):
    '''
    Connect to a repo and branch following a disconnect command.
    '''
    return call_az("az staticwebapp reconnect", locals())


def update(name, branch=None, no_wait=None, sku=None, source=None, tags=None, token=None):
    '''
    Update a static app. Return the app updated.
    '''
    return call_az("az staticwebapp update", locals())

