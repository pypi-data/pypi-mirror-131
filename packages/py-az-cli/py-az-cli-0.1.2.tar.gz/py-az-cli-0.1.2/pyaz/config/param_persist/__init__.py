from ... pyaz_utils import call_az

def on():
    '''
    Turn on parameter persistence.
    '''
    return call_az("az config param-persist on", locals())


def off():
    '''
    Turn off parameter persistence.
    '''
    return call_az("az config param-persist off", locals())


def show():
    '''
    Show parameter persistence data.
    '''
    return call_az("az config param-persist show", locals())


def delete(all=None, purge=None, recursive=None, yes=None):
    '''
    Delete parameter persistence data.
    '''
    return call_az("az config param-persist delete", locals())

