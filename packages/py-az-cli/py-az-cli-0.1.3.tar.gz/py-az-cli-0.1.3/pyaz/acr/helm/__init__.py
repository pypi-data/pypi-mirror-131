from ... pyaz_utils import _call_az
from . import repo


def list(name, password=None, repository=None, resource_group=None, suffix=None, username=None):
    '''
    List all helm charts in an Azure Container Registry.
    '''
    return _call_az("az acr helm list", locals())


def show(name, password=None, repository=None, resource_group=None, suffix=None, username=None, version=None):
    '''
    Describe a helm chart in an Azure Container Registry.
    '''
    return _call_az("az acr helm show", locals())


def delete(name, password=None, prov=None, repository=None, resource_group=None, suffix=None, username=None, version=None, yes=None):
    '''
    Delete a helm chart version in an Azure Container Registry.
    '''
    return _call_az("az acr helm delete", locals())


def push(name, force=None, password=None, repository=None, resource_group=None, suffix=None, username=None):
    '''
    Push a helm chart package to an Azure Container Registry.
    '''
    return _call_az("az acr helm push", locals())


def install_cli(client_version=None, install_location=None, yes=None):
    '''
    Download and install Helm command-line tool.
    '''
    return _call_az("az acr helm install-cli", locals())

