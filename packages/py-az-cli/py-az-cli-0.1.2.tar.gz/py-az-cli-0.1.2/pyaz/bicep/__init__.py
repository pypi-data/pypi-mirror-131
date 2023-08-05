from .. pyaz_utils import call_az

def install(target_platform=None, version=None):
    '''
    Install Bicep CLI.
    '''
    return call_az("az bicep install", locals())


def uninstall():
    '''
    Uninstall Bicep CLI.
    '''
    return call_az("az bicep uninstall", locals())


def upgrade(target_platform=None):
    '''
    Upgrade Bicep CLI to the latest version.
    '''
    return call_az("az bicep upgrade", locals())


def build(file, outdir=None, outfile=None, stdout=None):
    '''
    Build a Bicep file.
    '''
    return call_az("az bicep build", locals())


def decompile(file):
    '''
    Attempt to decompile an ARM template file to a Bicep file.
    '''
    return call_az("az bicep decompile", locals())


def publish(file, target):
    '''
    Publish a bicep file to a remote module registry.
    '''
    return call_az("az bicep publish", locals())


def version():
    '''
    Show the installed version of Bicep CLI.
    '''
    return call_az("az bicep version", locals())


def list_versions():
    '''
    List out all available versions of Bicep CLI.
    '''
    return call_az("az bicep list-versions", locals())

