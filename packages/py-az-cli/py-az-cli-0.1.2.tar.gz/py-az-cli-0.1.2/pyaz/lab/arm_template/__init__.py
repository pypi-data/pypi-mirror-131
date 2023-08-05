from ... pyaz_utils import call_az

def list(artifact_source_name, lab_name, resource_group, expand=None, filter=None, orderby=None, top=None):
    return call_az("az lab arm-template list", locals())


def show(artifact_source_name, lab_name, name, resource_group, export_parameters=None):
    '''
    Get the details of an ARM template in a lab.
    '''
    return call_az("az lab arm-template show", locals())

