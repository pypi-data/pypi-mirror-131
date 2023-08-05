from .... pyaz_utils import call_az

def show(location, name, publisher, version):
    return call_az("az vmss extension image show", locals())


def list_names(location, publisher):
    return call_az("az vmss extension image list-names", locals())


def list_versions(location, name, publisher, filter=None, orderby=None, top=None):
    return call_az("az vmss extension image list-versions", locals())


def list(latest=None, location=None, name=None, publisher=None, version=None):
    '''
    List the information on available extensions.
    '''
    return call_az("az vmss extension image list", locals())

