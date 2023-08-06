from ... pyaz_utils import _call_az

def list(resource_group, solution_name):
    '''
    List all yours IoT Security solution aggregated recommendations.
    '''
    return _call_az("az security iot-recommendations list", locals())


def show(name, resource_group, solution_name):
    '''
    Shows a single aggregated recommendation of yours IoT Security solution.
    '''
    return _call_az("az security iot-recommendations show", locals())

