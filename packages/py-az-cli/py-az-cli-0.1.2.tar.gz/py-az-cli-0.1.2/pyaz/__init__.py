from . pyaz_utils import call_az
from . import account, acr, acs, aks, apim, appconfig, aro, bicep, bot, cache, cdn, cloud, config, container, cosmosdb, demo, deployment, deployment_scripts, disk, disk_access, disk_encryption_set, dms, extension, feature, group, hdinsight, identity, image, keyvault, local_context, lock, logicapp, managedapp, network, openshift, ppg, provider, redis, resource, sig, signalr, snapshot, sql, sshkey, staticwebapp, storage, tag, term, ts, webapp


def configure(defaults=None, list_defaults=None, scope=None):
    '''
    Manage Azure CLI configuration. This command is interactive.
    '''
    return call_az("az configure", locals())


def feedback():
    '''
    Send feedback to the Azure CLI Team.
    '''
    return call_az("az feedback", locals())


def find():
    '''
    I'm an AI robot, my advice is based on our Azure documentation as well as the usage patterns of Azure CLI and Azure ARM users. Using me improves Azure products and documentation.
    '''
    return call_az("az find", locals())


def interactive(style=None, update=None):
    '''
    Start interactive mode. Installs the Interactive extension if not installed already.
    '''
    return call_az("az interactive", locals())


def login(allow_no_subscriptions=None, federated_token=None, password=None, scope=None, service_principal=None, tenant=None, use_cert_sn_issuer=None, use_device_code=None, username=None):
    '''
    Log in to Azure.
    '''
    return call_az("az login", locals())


def logout(username=None):
    return call_az("az logout", locals())


def self_test():
    '''
    Runs a self-test of the CLI.
    '''
    return call_az("az self-test", locals())


def rest(url, body=None, headers=None, method=None, output_file=None, resource=None, skip_authorization_header=None, uri_parameters=None):
    '''
    Invoke a custom request.
    '''
    return call_az("az rest", locals())


def version():
    '''
    Show the versions of Azure CLI modules and extensions in JSON format by default or format configured by --output
    '''
    return call_az("az version", locals())


def upgrade(all=None, yes=None):
    '''
    Upgrade Azure CLI and extensions
    '''
    return call_az("az upgrade", locals())

