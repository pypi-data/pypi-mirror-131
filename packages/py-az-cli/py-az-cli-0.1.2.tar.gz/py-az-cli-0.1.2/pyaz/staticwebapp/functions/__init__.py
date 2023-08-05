from ... pyaz_utils import call_az

def link(function_resource_id, name, resource_group, force=None):
    '''
    Link an Azure Function to a static webapp. Also known as "Bring your own Functions." Only one Azure Functions app is available to a single static web app. Static webapp SKU must be "Standard"
    '''
    return call_az("az staticwebapp functions link", locals())


def unlink(name, resource_group):
    '''
    Unlink an Azure Function from a static webapp
    '''
    return call_az("az staticwebapp functions unlink", locals())


def show(name, resource_group):
    '''
    Show details on the Azure Function linked to a static webapp
    '''
    return call_az("az staticwebapp functions show", locals())

