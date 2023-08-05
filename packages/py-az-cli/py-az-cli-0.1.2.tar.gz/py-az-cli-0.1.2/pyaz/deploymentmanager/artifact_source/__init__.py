from ... pyaz_utils import call_az

def create(artifact_source_name, location, resource_group, sas_uri, artifact_root=None, tags=None):
    '''
    Creates an artifact source.
    '''
    return call_az("az deploymentmanager artifact-source create", locals())


def delete(artifact_source_name, resource_group, yes=None):
    '''
    Deletes an artifact source.
    '''
    return call_az("az deploymentmanager artifact-source delete", locals())


def show(artifact_source_name, resource_group):
    '''
    Get the details of an artifact source.
    '''
    return call_az("az deploymentmanager artifact-source show", locals())


def list(resource_group):
    '''
    List all artifact sources in a resource group.
    '''
    return call_az("az deploymentmanager artifact-source list", locals())


def update(artifact_source_name, resource_group, add=None, artifact_root=None, force_string=None, remove=None, sas_uri=None, set=None, tags=None):
    '''
    Updates an artifact source.
    '''
    return call_az("az deploymentmanager artifact-source update", locals())

