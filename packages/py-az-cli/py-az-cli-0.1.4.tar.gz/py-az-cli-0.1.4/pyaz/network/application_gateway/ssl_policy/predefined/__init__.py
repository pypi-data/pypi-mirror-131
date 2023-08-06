from ..... pyaz_utils import _call_az

def list():
    '''
    Lists all SSL predefined policies for configuring SSL policy.
    '''
    return _call_az("az network application-gateway ssl-policy predefined list", locals())


def show(name):
    '''
    Gets SSL predefined policy with the specified policy name.
    '''
    return _call_az("az network application-gateway ssl-policy predefined show", locals())

