from ... pyaz_utils import _call_az

def list(filter=None, skiptoken=None, top=None):
    return _call_az("az billing period list", locals())


def show(name):
    return _call_az("az billing period show", locals())

