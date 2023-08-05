from ... pyaz_utils import call_az

def list(device_name, resource_group):
    '''
    Get all the alerts for a Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge alert list", locals())


def show(device_name, name, resource_group):
    '''
    Get an alert by name.
    '''
    return call_az("az databoxedge alert show", locals())

