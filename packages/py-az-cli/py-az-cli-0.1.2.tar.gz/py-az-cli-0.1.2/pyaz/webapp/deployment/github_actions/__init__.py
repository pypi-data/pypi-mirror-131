from .... pyaz_utils import call_az

def add(name, repo, resource_group, branch=None, force=None, login_with_github=None, runtime=None, slot=None, token=None):
    '''
    Add a GitHub Actions workflow file to the specified repository. The workflow will build and deploy your app to the specified webapp.
    '''
    return call_az("az webapp deployment github-actions add", locals())


def remove(name, repo, resource_group, branch=None, login_with_github=None, slot=None, token=None):
    '''
    Remove and disconnect the GitHub Actions workflow file from the specified repository.
    '''
    return call_az("az webapp deployment github-actions remove", locals())

