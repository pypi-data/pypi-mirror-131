from .... pyaz_utils import call_az

def config_local_git(name, resource_group, slot=None):
    '''
    Get a URL for a git repository endpoint to clone and push to for web app deployment.
    '''
    return call_az("az webapp deployment source config-local-git", locals())


def config_zip(name, resource_group, src, slot=None, timeout=None):
    '''
    Perform deployment using the kudu zip push deployment for a web app.
    '''
    return call_az("az webapp deployment source config-zip", locals())


def config(name, repo_url, resource_group, branch=None, git_token=None, github_action=None, manual_integration=None, repository_type=None, slot=None):
    '''
    Manage deployment from git or Mercurial repositories.
    '''
    return call_az("az webapp deployment source config", locals())


def sync(name, resource_group, slot=None):
    '''
    Synchronize from the repository. Only needed under manual integration mode.
    '''
    return call_az("az webapp deployment source sync", locals())


def show(name, resource_group, slot=None):
    '''
    Get the details of a source control deployment configuration.
    '''
    return call_az("az webapp deployment source show", locals())


def delete(name, resource_group, slot=None):
    '''
    Delete a source control deployment configuration.
    '''
    return call_az("az webapp deployment source delete", locals())


def update_token(git_token=None):
    return call_az("az webapp deployment source update-token", locals())

