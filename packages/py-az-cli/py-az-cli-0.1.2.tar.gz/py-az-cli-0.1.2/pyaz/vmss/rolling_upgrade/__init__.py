from ... pyaz_utils import call_az

def cancel(name, resource_group):
    return call_az("az vmss rolling-upgrade cancel", locals())


def get_latest(name, resource_group):
    return call_az("az vmss rolling-upgrade get-latest", locals())


def start(name, resource_group):
    return call_az("az vmss rolling-upgrade start", locals())

