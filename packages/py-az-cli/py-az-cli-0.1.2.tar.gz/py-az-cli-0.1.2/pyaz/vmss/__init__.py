from .. pyaz_utils import call_az
from . import application, diagnostics, disk, encryption, extension, identity, nic, rolling_upgrade, run_command


def create(name, resource_group, accelerated_networking=None, admin_password=None, admin_username=None, app_gateway=None, app_gateway_capacity=None, app_gateway_sku=None, app_gateway_subnet_address_prefix=None, asgs=None, assign_identity=None, authentication_type=None, automatic_repairs_grace_period=None, backend_pool_name=None, backend_port=None, capacity_reservation_group=None, computer_name_prefix=None, custom_data=None, data_disk_caching=None, data_disk_encryption_sets=None, data_disk_iops=None, data_disk_mbps=None, data_disk_sizes_gb=None, disable_overprovision=None, dns_servers=None, edge_zone=None, enable_agent=None, enable_auto_update=None, enable_cross_zone_upgrade=None, enable_spot_restore=None, encryption_at_host=None, ephemeral_os_disk=None, ephemeral_os_disk_placement=None, eviction_policy=None, generate_ssh_keys=None, health_probe=None, host_group=None, image=None, instance_count=None, lb_nat_pool_name=None, lb_sku=None, license_type=None, load_balancer=None, location=None, max_batch_instance_percent=None, max_price=None, max_unhealthy_instance_percent=None, max_unhealthy_upgraded_instance_percent=None, network_api_version=None, no_wait=None, nsg=None, orchestration_mode=None, os_disk_caching=None, os_disk_encryption_set=None, os_disk_name=None, os_disk_size_gb=None, os_type=None, patch_mode=None, pause_time_between_batches=None, plan_name=None, plan_product=None, plan_promotion_code=None, plan_publisher=None, platform_fault_domain_count=None, ppg=None, prioritize_unhealthy_instances=None, priority=None, public_ip_address=None, public_ip_address_allocation=None, public_ip_address_dns_name=None, public_ip_per_vm=None, role=None, scale_in_policy=None, scope=None, secrets=None, single_placement_group=None, specialized=None, spot_restore_timeout=None, ssh_dest_key_path=None, ssh_key_values=None, storage_container_name=None, storage_sku=None, subnet=None, subnet_address_prefix=None, tags=None, terminate_notification_time=None, ultra_ssd_enabled=None, upgrade_policy_mode=None, use_unmanaged_disk=None, user_data=None, validate=None, vm_domain_name=None, vm_sku=None, vnet_address_prefix=None, vnet_name=None, zones=None):
    '''
    Create an Azure Virtual Machine Scale Set.
    '''
    return call_az("az vmss create", locals())


def deallocate(name, resource_group, instance_ids=None, no_wait=None):
    '''
    Deallocate VMs within a VMSS.
    '''
    return call_az("az vmss deallocate", locals())


def delete(name, resource_group, force_deletion=None, no_wait=None):
    return call_az("az vmss delete", locals())


def delete_instances(instance_ids, name, resource_group, no_wait=None):
    '''
    Delete VMs within a VMSS.
    '''
    return call_az("az vmss delete-instances", locals())


def get_instance_view(name, resource_group, instance_id=None):
    '''
    View an instance of a VMSS.
    '''
    return call_az("az vmss get-instance-view", locals())


def list(resource_group=None):
    '''
    List VMSS.
    '''
    return call_az("az vmss list", locals())


def list_instances(name, resource_group, expand=None, filter=None, select=None):
    '''
    Get a list of all virtual machines in a VM scale sets.
    '''
    return call_az("az vmss list-instances", locals())


def list_instance_connection_info(name, resource_group):
    '''
    Get the IP address and port number used to connect to individual VM instances within a set.
    '''
    return call_az("az vmss list-instance-connection-info", locals())


def list_instance_public_ips(name, resource_group):
    '''
    List public IP addresses of VM instances within a set.
    '''
    return call_az("az vmss list-instance-public-ips", locals())


def list_skus(name, resource_group):
    return call_az("az vmss list-skus", locals())


def reimage(name, resource_group, instance_id=None, no_wait=None):
    '''
    Reimage VMs within a VMSS.
    '''
    return call_az("az vmss reimage", locals())


def perform_maintenance(name, resource_group, vm_instance_i_ds=None):
    return call_az("az vmss perform-maintenance", locals())


def restart(name, resource_group, instance_ids=None, no_wait=None):
    '''
    Restart VMs within a VMSS.
    '''
    return call_az("az vmss restart", locals())


def scale(name, new_capacity, resource_group, no_wait=None):
    '''
    Change the number of VMs within a VMSS.
    '''
    return call_az("az vmss scale", locals())


def show(name, resource_group, include_user_data=None, instance_id=None):
    '''
    Get details on VMs within a VMSS.
    '''
    return call_az("az vmss show", locals())


def simulate_eviction(instance_id, name, resource_group):
    '''
    Simulate the eviction of a Spot virtual machine in a VM scale set.
    '''
    return call_az("az vmss simulate-eviction", locals())


def start(name, resource_group, instance_ids=None, no_wait=None):
    '''
    Start VMs within a VMSS.
    '''
    return call_az("az vmss start", locals())


def stop(name, resource_group, instance_ids=None, no_wait=None, skip_shutdown=None):
    '''
    Power off (stop) VMs within a VMSS.
    '''
    return call_az("az vmss stop", locals())


def update(name, resource_group, add=None, automatic_repairs_grace_period=None, capacity_reservation_group=None, enable_automatic_repairs=None, enable_cross_zone_upgrade=None, enable_spot_restore=None, enable_terminate_notification=None, ephemeral_os_disk_placement=None, force_string=None, instance_id=None, license_type=None, max_batch_instance_percent=None, max_price=None, max_unhealthy_instance_percent=None, max_unhealthy_upgraded_instance_percent=None, no_wait=None, pause_time_between_batches=None, ppg=None, prioritize_unhealthy_instances=None, priority=None, protect_from_scale_in=None, protect_from_scale_set_actions=None, remove=None, scale_in_policy=None, set=None, spot_restore_timeout=None, terminate_notification_time=None, ultra_ssd_enabled=None, user_data=None, vm_sku=None):
    '''
    Update a VMSS. Run 'az vmss update-instances' command to roll out the changes to VMs if you have not configured upgrade policy.
    '''
    return call_az("az vmss update", locals())


def update_instances(instance_ids, name, resource_group, no_wait=None):
    '''
    Upgrade VMs within a VMSS.
    '''
    return call_az("az vmss update-instances", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, instance_id=None, interval=None, timeout=None, updated=None):
    '''
    Place the CLI in a waiting state until a condition of a scale set is met.
    '''
    return call_az("az vmss wait", locals())


def get_os_upgrade_history(name, resource_group):
    return call_az("az vmss get-os-upgrade-history", locals())


def set_orchestration_service_state(action, name, resource_group, service_name, no_wait=None):
    '''
    Change ServiceState property for a given service within a VMSS.
    '''
    return call_az("az vmss set-orchestration-service-state", locals())

