from ... pyaz_utils import call_az

def create(allow_force_push=None, functionapp_name=None, github_pat=None, github_repository=None, organization_name=None, overwrite_yaml=None, project_name=None, repository_name=None):
    'Create an Azure DevOps pipeline for a function app.'
    return call_az("az functionapp devops-pipeline create", locals())

