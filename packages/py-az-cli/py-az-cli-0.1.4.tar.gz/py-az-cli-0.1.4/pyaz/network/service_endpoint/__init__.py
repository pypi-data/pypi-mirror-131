from ... pyaz_utils import _call_az
from . import policy, policy_definition


def list(location):
    return _call_az("az network service-endpoint list", locals())

