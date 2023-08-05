from ... pyaz_utils import call_az

def list():
    return call_az("az cdn edge-node list", locals())

