from ... pyaz_utils import _call_az

def list(resource_group, solution_name):
    '''
    List all IoT security Analytics metrics.
    '''
    return _call_az("az security iot-analytics list", locals())


def show(resource_group, solution_name):
    '''
    Shows IoT Security Analytics metrics.
    '''
    return _call_az("az security iot-analytics show", locals())

