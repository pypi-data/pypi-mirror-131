from ... pyaz_utils import call_az

def list():
    return call_az("az billing enrollment-account list", locals())


def show(name):
    return call_az("az billing enrollment-account show", locals())

