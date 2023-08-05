from .. pyaz_utils import call_az

def on():
    '''
    Turn on local context
    '''
    return call_az("az local-context on", locals())


def off():
    '''
    Turn off local context
    '''
    return call_az("az local-context off", locals())


def show(name=None):
    '''
    Show local context data
    '''
    return call_az("az local-context show", locals())


def delete(all=None, name=None, purge=None, recursive=None, yes=None):
    '''
    Delete local context data
    '''
    return call_az("az local-context delete", locals())

