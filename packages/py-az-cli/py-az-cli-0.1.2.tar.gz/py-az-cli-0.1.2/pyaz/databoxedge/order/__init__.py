from ... pyaz_utils import call_az

def list(device_name, resource_group):
    '''
    List all the orders related to a Data Box Edge/Data Box Gateway device.
    '''
    return call_az("az databoxedge order list", locals())


def show(device_name, resource_group):
    '''
    Get a specific order by name.
    '''
    return call_az("az databoxedge order show", locals())


def create(address_line1, city, company_name, contact_person, country, device_name, email_list, phone, postal_code, resource_group, state, status, address_line2=None, address_line3=None, comments=None, no_wait=None):
    '''
    Create an order.
    '''
    return call_az("az databoxedge order create", locals())


def update(device_name, resource_group, add=None, address_line1=None, address_line2=None, address_line3=None, city=None, comments=None, company_name=None, contact_person=None, country=None, email_list=None, force_string=None, no_wait=None, phone=None, postal_code=None, remove=None, set=None, state=None, status=None):
    '''
    Update an order.
    '''
    return call_az("az databoxedge order update", locals())


def delete(device_name, resource_group, no_wait=None, yes=None):
    '''
    Delete the order related to the device.
    '''
    return call_az("az databoxedge order delete", locals())


def wait(device_name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the databoxedge order is met.
    '''
    return call_az("az databoxedge order wait", locals())

