from ... pyaz_utils import _call_az

def list():
    return _call_az("az billing enrollment-account list", locals())


def show(name):
    return _call_az("az billing enrollment-account show", locals())

