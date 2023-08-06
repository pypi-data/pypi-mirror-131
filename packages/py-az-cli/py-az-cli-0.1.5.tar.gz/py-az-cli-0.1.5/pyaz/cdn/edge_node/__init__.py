from ... pyaz_utils import _call_az

def list():
    return _call_az("az cdn edge-node list", locals())

