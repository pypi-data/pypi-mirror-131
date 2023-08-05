from .... pyaz_utils import call_az

def config_local_git(name, resource_group, slot=None):
    '''
    Get a URL for a git repository endpoint to clone and push to for function app deployment.
    '''
    return call_az("az functionapp deployment source config-local-git", locals())


def config_zip(name, resource_group, src, build_remote=None, slot=None, timeout=None):
    '''
    Perform deployment using the kudu zip push deployment for a function app.
    '''
    return call_az("az functionapp deployment source config-zip", locals())


def config(name, repo_url, resource_group, branch=None, git_token=None, github_action=None, manual_integration=None, repository_type=None, slot=None):
    '''
    Manage deployment from git or Mercurial repositories.
    '''
    return call_az("az functionapp deployment source config", locals())


def sync(name, resource_group, slot=None):
    '''
    Synchronize from the repository. Only needed under manual integration mode.
    '''
    return call_az("az functionapp deployment source sync", locals())


def show(name, resource_group, slot=None):
    '''
    Get the details of a source control deployment configuration.
    '''
    return call_az("az functionapp deployment source show", locals())


def delete(name, resource_group, slot=None):
    '''
    Delete a source control deployment configuration.
    '''
    return call_az("az functionapp deployment source delete", locals())


def update_token(git_token=None):
    return call_az("az functionapp deployment source update-token", locals())

