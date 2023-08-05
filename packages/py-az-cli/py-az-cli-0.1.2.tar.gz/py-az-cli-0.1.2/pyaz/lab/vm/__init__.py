from ... pyaz_utils import call_az

def show(lab_name, name, resource_group, expand=None):
    return call_az("az lab vm show", locals())


def delete(lab_name, name, resource_group):
    return call_az("az lab vm delete", locals())


def start(lab_name, name, resource_group):
    return call_az("az lab vm start", locals())


def stop(lab_name, name, resource_group):
    return call_az("az lab vm stop", locals())


def apply_artifacts(lab_name, name, resource_group, artifacts=None):
    '''
    Apply artifacts to a virtual machine in Azure DevTest Lab.
    '''
    return call_az("az lab vm apply-artifacts", locals())


def list(lab_name, resource_group, all=None, claimable=None, environment=None, expand=None, filters=None, object_id=None, order_by=None, top=None):
    '''
    List the VMs in an Azure DevTest Lab.
    '''
    return call_az("az lab vm list", locals())


def claim(lab_name=None, name=None, resource_group=None):
    '''
    Claim a virtual machine from the Lab.
    '''
    return call_az("az lab vm claim", locals())


def create(lab_name, name, resource_group, admin_password=None, admin_username=None, allow_claim=None, artifacts=None, authentication_type=None, disk_type=None, expiration_date=None, formula=None, generate_ssh_keys=None, image=None, image_type=None, ip_configuration=None, notes=None, saved_secret=None, size=None, ssh_key=None, subnet=None, tags=None, vnet_name=None):
    '''
    Create a VM in a lab.
    '''
    return call_az("az lab vm create", locals())

