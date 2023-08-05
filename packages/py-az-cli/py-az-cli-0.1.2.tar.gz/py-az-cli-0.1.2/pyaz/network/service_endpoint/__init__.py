from ... pyaz_utils import call_az
from . import policy, policy_definition


def list(location):
    return call_az("az network service-endpoint list", locals())

