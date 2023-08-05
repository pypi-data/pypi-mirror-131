from ... pyaz_utils import call_az

def list(filter=None, skiptoken=None, top=None):
    return call_az("az billing period list", locals())


def show(name):
    return call_az("az billing period show", locals())

