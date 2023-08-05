from ... pyaz_utils import call_az

def list(resource_group, solution_name):
    '''
    List all yours IoT Security solution aggregated alerts.
    '''
    return call_az("az security iot-alerts list", locals())


def show(name, resource_group, solution_name):
    '''
    Shows a single aggregated alert of yours IoT Security solution.
    '''
    return call_az("az security iot-alerts show", locals())


def delete(name, resource_group, solution_name):
    '''
    Dismiss an aggregated IoT Security Alert.
    '''
    return call_az("az security iot-alerts delete", locals())

