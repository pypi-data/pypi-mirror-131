from .. pyaz_utils import call_az
from . import application, availability_set, boot_diagnostics, diagnostics, disk, encryption, extension, host, identity, image, nic, run_command, secret, unmanaged_disk, user


def capture(name, resource_group, vhd_name_prefix, overwrite=None, storage_container=None):
    '''
    Capture information for a stopped VM.
    '''
    return call_az("az vm capture", locals())


def create(name, resource_group, accelerated_networking=None, admin_password=None, admin_username=None, asgs=None, assign_identity=None, attach_data_disks=None, attach_os_disk=None, authentication_type=None, availability_set=None, boot_diagnostics_storage=None, capacity_reservation_group=None, computer_name=None, count=None, custom_data=None, data_disk_caching=None, data_disk_delete_option=None, data_disk_encryption_sets=None, data_disk_sizes_gb=None, edge_zone=None, enable_agent=None, enable_auto_update=None, enable_hibernation=None, enable_hotpatching=None, enable_secure_boot=None, enable_vtpm=None, encryption_at_host=None, ephemeral_os_disk=None, ephemeral_os_disk_placement=None, eviction_policy=None, generate_ssh_keys=None, host=None, host_group=None, image=None, license_type=None, location=None, max_price=None, nic_delete_option=None, nics=None, no_wait=None, nsg=None, nsg_rule=None, os_disk_caching=None, os_disk_delete_option=None, os_disk_encryption_set=None, os_disk_name=None, os_disk_size_gb=None, os_type=None, patch_mode=None, plan_name=None, plan_product=None, plan_promotion_code=None, plan_publisher=None, platform_fault_domain=None, ppg=None, priority=None, private_ip_address=None, public_ip_address=None, public_ip_address_allocation=None, public_ip_address_dns_name=None, public_ip_sku=None, role=None, scope=None, secrets=None, security_type=None, size=None, specialized=None, ssh_dest_key_path=None, ssh_key_name=None, ssh_key_values=None, storage_account=None, storage_container_name=None, storage_sku=None, subnet=None, subnet_address_prefix=None, tags=None, ultra_ssd_enabled=None, use_unmanaged_disk=None, user_data=None, validate=None, vmss=None, vnet_address_prefix=None, vnet_name=None, workspace=None, zone=None):
    '''
    Create an Azure Virtual Machine.
    '''
    return call_az("az vm create", locals())


def convert(name, resource_group):
    '''
    Convert a VM with unmanaged disks to use managed disks.
    '''
    return call_az("az vm convert", locals())


def deallocate(name, resource_group, hibernate=None, no_wait=None):
    '''
    Deallocate a VM.
    '''
    return call_az("az vm deallocate", locals())


def delete(name, resource_group, force_deletion=None, no_wait=None, yes=None):
    '''
    Delete a VM.
    '''
    return call_az("az vm delete", locals())


def generalize(name, resource_group, no_wait=None):
    '''
    Mark a VM as generalized, allowing it to be imaged for multiple deployments.
    '''
    return call_az("az vm generalize", locals())


def get_instance_view(name, resource_group):
    '''
    Get instance information about a VM.
    '''
    return call_az("az vm get-instance-view", locals())


def list(resource_group=None, show_details=None):
    '''
    List details of Virtual Machines.
    '''
    return call_az("az vm list", locals())


def list_ip_addresses(name=None, resource_group=None):
    '''
    List IP addresses associated with a VM.
    '''
    return call_az("az vm list-ip-addresses", locals())


def list_sizes(location):
    '''
    List available sizes for VMs.
    '''
    return call_az("az vm list-sizes", locals())


def list_skus(all=None, location=None, resource_type=None, size=None, zone=None):
    '''
    Get details for compute-related resource SKUs.
    '''
    return call_az("az vm list-skus", locals())


def list_usage(location):
    '''
    List available usage resources for VMs.
    '''
    return call_az("az vm list-usage", locals())


def list_vm_resize_options(name, resource_group):
    '''
    List available resizing options for VMs.
    '''
    return call_az("az vm list-vm-resize-options", locals())


def open_port(name, port, resource_group, apply_to_subnet=None, nsg_name=None, priority=None):
    '''
    Opens a VM to inbound traffic on specified ports.
    '''
    return call_az("az vm open-port", locals())


def perform_maintenance(name, resource_group):
    return call_az("az vm perform-maintenance", locals())


def redeploy(name, resource_group, no_wait=None):
    '''
    Redeploy an existing VM.
    '''
    return call_az("az vm redeploy", locals())


def resize(name, resource_group, size, no_wait=None):
    '''
    Update a VM's size.
    '''
    return call_az("az vm resize", locals())


def restart(name, resource_group, force=None, no_wait=None):
    '''
    Restart VMs.
    '''
    return call_az("az vm restart", locals())


def show(name, resource_group, include_user_data=None, show_details=None):
    '''
    Get the details of a VM.
    '''
    return call_az("az vm show", locals())


def simulate_eviction(name, resource_group):
    '''
    Simulate the eviction of a Spot VM.
    '''
    return call_az("az vm simulate-eviction", locals())


def start(name, resource_group, no_wait=None):
    '''
    Start a stopped VM.
    '''
    return call_az("az vm start", locals())


def stop(name, resource_group, no_wait=None, skip_shutdown=None):
    '''
    Power off (stop) a running VM.
    '''
    return call_az("az vm stop", locals())


def reapply(name, resource_group, no_wait=None):
    '''
    Reapply VMs.
    '''
    return call_az("az vm reapply", locals())


def update(name, resource_group, add=None, capacity_reservation_group=None, disk_caching=None, enable_hibernation=None, enable_secure_boot=None, enable_vtpm=None, ephemeral_os_disk_placement=None, force_string=None, host=None, host_group=None, license_type=None, max_price=None, no_wait=None, os_disk=None, ppg=None, priority=None, remove=None, set=None, size=None, ultra_ssd_enabled=None, user_data=None, workspace=None, write_accelerator=None):
    '''
    Update the properties of a VM.
    '''
    return call_az("az vm update", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of the VM is met.
    '''
    return call_az("az vm wait", locals())


def auto_shutdown(name, resource_group, email=None, location=None, off=None, time=None, webhook=None):
    '''
    Manage auto-shutdown for VM.
    '''
    return call_az("az vm auto-shutdown", locals())


def assess_patches(name, resource_group):
    '''
    Assess patches on a VM.
    '''
    return call_az("az vm assess-patches", locals())


def install_patches(maximum_duration, name, reboot_setting, resource_group, classifications_to_include_linux=None, classifications_to_include_win=None, exclude_kbs_requiring_reboot=None, kb_numbers_to_exclude=None, kb_numbers_to_include=None, no_wait=None, package_name_masks_to_exclude=None, package_name_masks_to_include=None):
    '''
    Install patches on a VM.
    '''
    return call_az("az vm install-patches", locals())

