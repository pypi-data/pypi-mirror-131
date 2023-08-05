from ... pyaz_utils import call_az

def list(account_name, profile_name):
    '''
    List the instructions by billing profile id.
    '''
    return call_az("az billing instruction list", locals())


def show(account_name, name, profile_name):
    '''
    Show the instruction by name. These are custom billing instructions and are only applicable for certain customers.
    '''
    return call_az("az billing instruction show", locals())


def create(account_name, name, profile_name, amount=None, creation_date=None, end_date=None, start_date=None):
    '''
    Create an instruction. These are custom billing instructions and are only applicable for certain customers.
    '''
    return call_az("az billing instruction create", locals())


def update(account_name, name, profile_name, add=None, amount=None, creation_date=None, end_date=None, force_string=None, remove=None, set=None, start_date=None):
    '''
    Update an instruction. These are custom billing instructions and are only applicable for certain customers.
    '''
    return call_az("az billing instruction update", locals())

