from ..... pyaz_utils import call_az

def show(circuit_name, name, peering_name, resource_group):
    return call_az("az network express-route peering peer-connection show", locals())


def list(circuit_name, peering_name, resource_group):
    return call_az("az network express-route peering peer-connection list", locals())

