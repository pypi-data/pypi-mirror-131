from ... pyaz_utils import call_az

def list():
    '''
    List security contact.
    '''
    return call_az("az security contact list", locals())


def show(name):
    '''
    Shows a security contact.
    '''
    return call_az("az security contact show", locals())


def create(email, name, alert_notifications=None, alerts_admins=None, phone=None):
    '''
    Creates a security contact.
    '''
    return call_az("az security contact create", locals())


def delete(name):
    '''
    Deletes a security contact.
    '''
    return call_az("az security contact delete", locals())

