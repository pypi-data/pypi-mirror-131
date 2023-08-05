from ... pyaz_utils import call_az
from . import deployment


def tail(name, resource_group, provider=None, slot=None):
    '''
    Start live log tracing for a web app.
    '''
    return call_az("az webapp log tail", locals())


def download(name, resource_group, log_file=None, slot=None):
    '''
    Download a web app's log history as a zip file.
    '''
    return call_az("az webapp log download", locals())


def config(name, resource_group, application_logging=None, detailed_error_messages=None, docker_container_logging=None, failed_request_tracing=None, level=None, slot=None, web_server_logging=None):
    '''
    Configure logging for a web app.
    '''
    return call_az("az webapp log config", locals())


def show(name, resource_group, slot=None):
    '''
    Get the details of a web app's logging configuration.
    '''
    return call_az("az webapp log show", locals())

