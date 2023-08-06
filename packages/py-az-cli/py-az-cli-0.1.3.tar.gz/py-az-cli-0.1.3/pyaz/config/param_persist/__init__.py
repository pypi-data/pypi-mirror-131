from ... pyaz_utils import _call_az

def on():
    '''
    Turn on parameter persistence.
    '''
    return _call_az("az config param-persist on", locals())


def off():
    '''
    Turn off parameter persistence.
    '''
    return _call_az("az config param-persist off", locals())


def show():
    '''
    Show parameter persistence data.
    '''
    return _call_az("az config param-persist show", locals())


def delete(all=None, purge=None, recursive=None, yes=None):
    '''
    Delete parameter persistence data.
    '''
    return _call_az("az config param-persist delete", locals())

