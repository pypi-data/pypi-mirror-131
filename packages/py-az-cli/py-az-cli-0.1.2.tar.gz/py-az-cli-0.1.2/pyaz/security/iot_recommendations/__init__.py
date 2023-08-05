from ... pyaz_utils import call_az

def list(resource_group, solution_name):
    '''
    List all yours IoT Security solution aggregated recommendations.
    '''
    return call_az("az security iot-recommendations list", locals())


def show(name, resource_group, solution_name):
    '''
    Shows a single aggregated recommendation of yours IoT Security solution.
    '''
    return call_az("az security iot-recommendations show", locals())

