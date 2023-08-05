from .... pyaz_utils import call_az

def show(location, name, publisher, version):
    '''
    Display information for an extension.
    '''
    return call_az("az vm extension image show", locals())


def list_names(location, publisher):
    '''
    List the names of available extensions.
    '''
    return call_az("az vm extension image list-names", locals())


def list_versions(location, name, publisher, filter=None, orderby=None, top=None):
    '''
    List the versions for available extensions.
    '''
    return call_az("az vm extension image list-versions", locals())


def list(latest=None, location=None, name=None, publisher=None, version=None):
    '''
    List the information on available extensions.
    '''
    return call_az("az vm extension image list", locals())

