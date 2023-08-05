from .. pyaz_utils import call_az
from . import command, nodepool


def browse(name, resource_group, disable_browser=None, listen_address=None, listen_port=None):
    '''
    Show the dashboard for a Kubernetes cluster in a web browser.
    '''
    return call_az("az aks browse", locals())


def create(name, resource_group, aad_admin_group_object_ids=None, aad_client_app_id=None, aad_server_app_id=None, aad_server_app_secret=None, aad_tenant_id=None, aci_subnet_name=None, admin_username=None, aks_custom_headers=None, api_server_authorized_ip_ranges=None, appgw_id=None, appgw_name=None, appgw_subnet_cidr=None, appgw_subnet_id=None, appgw_watch_namespace=None, assign_identity=None, assign_kubelet_identity=None, attach_acr=None, auto_upgrade_channel=None, client_secret=None, cluster_autoscaler_profile=None, disable_local_accounts=None, disable_public_fqdn=None, disable_rbac=None, dns_name_prefix=None, dns_service_ip=None, docker_bridge_address=None, edge_zone=None, enable_aad=None, enable_addons=None, enable_ahub=None, enable_azure_rbac=None, enable_cluster_autoscaler=None, enable_encryption_at_host=None, enable_managed_identity=None, enable_node_public_ip=None, enable_private_cluster=None, enable_rbac=None, enable_secret_rotation=None, enable_sgxquotehelper=None, enable_ultra_ssd=None, fqdn_subdomain=None, generate_ssh_keys=None, kubernetes_version=None, load_balancer_idle_timeout=None, load_balancer_managed_outbound_ip_count=None, load_balancer_outbound_ip_prefixes=None, load_balancer_outbound_ips=None, load_balancer_outbound_ports=None, load_balancer_sku=None, location=None, max_count=None, max_pods=None, min_count=None, network_plugin=None, network_policy=None, no_ssh_key=None, no_wait=None, node_count=None, node_osdisk_diskencryptionset_id=None, node_osdisk_size=None, node_osdisk_type=None, node_public_ip_prefix_id=None, node_vm_size=None, nodepool_labels=None, nodepool_name=None, nodepool_tags=None, os_sku=None, outbound_type=None, pod_cidr=None, ppg=None, private_dns_zone=None, rotation_poll_interval=None, service_cidr=None, service_principal=None, skip_subnet_role_assignment=None, ssh_key_value=None, tags=None, uptime_sla=None, vm_set_type=None, vnet_subnet_id=None, windows_admin_password=None, windows_admin_username=None, workspace_resource_id=None, yes=None, zones=None):
    '''
    Create a new managed Kubernetes cluster.
    '''
    return call_az("az aks create", locals())


def update(name, resource_group, aad_admin_group_object_ids=None, aad_tenant_id=None, aks_custom_headers=None, api_server_authorized_ip_ranges=None, assign_identity=None, attach_acr=None, auto_upgrade_channel=None, cluster_autoscaler_profile=None, detach_acr=None, disable_ahub=None, disable_azure_rbac=None, disable_cluster_autoscaler=None, disable_local_accounts=None, disable_public_fqdn=None, disable_secret_rotation=None, enable_aad=None, enable_ahub=None, enable_azure_rbac=None, enable_cluster_autoscaler=None, enable_local_accounts=None, enable_managed_identity=None, enable_public_fqdn=None, enable_secret_rotation=None, load_balancer_idle_timeout=None, load_balancer_managed_outbound_ip_count=None, load_balancer_outbound_ip_prefixes=None, load_balancer_outbound_ips=None, load_balancer_outbound_ports=None, max_count=None, min_count=None, no_uptime_sla=None, no_wait=None, nodepool_labels=None, rotation_poll_interval=None, tags=None, update_cluster_autoscaler=None, uptime_sla=None, windows_admin_password=None, yes=None):
    '''
    Update a managed Kubernetes cluster.
    '''
    return call_az("az aks update", locals())


def delete(name, resource_group, no_wait=None, yes=None):
    '''
    Delete a managed Kubernetes cluster.
    '''
    return call_az("az aks delete", locals())


def update_credentials(name, resource_group, aad_client_app_id=None, aad_server_app_id=None, aad_server_app_secret=None, aad_tenant_id=None, client_secret=None, no_wait=None, reset_aad=None, reset_service_principal=None, service_principal=None):
    '''
    Update credentials for a managed Kubernetes cluster, like service principal.
    '''
    return call_az("az aks update-credentials", locals())


def disable_addons(addons, name, resource_group, no_wait=None):
    '''
    Disable Kubernetes addons.
    '''
    return call_az("az aks disable-addons", locals())


def enable_addons(addons, name, resource_group, appgw_id=None, appgw_name=None, appgw_subnet_cidr=None, appgw_subnet_id=None, appgw_watch_namespace=None, enable_secret_rotation=None, enable_sgxquotehelper=None, no_wait=None, rotation_poll_interval=None, subnet_name=None, workspace_resource_id=None):
    '''
    Enable Kubernetes addons.
    '''
    return call_az("az aks enable-addons", locals())


def get_credentials(name, resource_group, admin=None, context=None, file=None, overwrite_existing=None, public_fqdn=None):
    '''
    Get access credentials for a managed Kubernetes cluster.
    '''
    return call_az("az aks get-credentials", locals())


def check_acr(acr, name, resource_group):
    '''
    Validate an ACR is accessible from an AKS cluster.
    '''
    return call_az("az aks check-acr", locals())


def get_upgrades(name, resource_group):
    '''
    Get the upgrade versions available for a managed Kubernetes cluster.
    '''
    return call_az("az aks get-upgrades", locals())


def install_cli(base_src_url=None, client_version=None, install_location=None, kubelogin_base_src_url=None, kubelogin_install_location=None, kubelogin_version=None):
    '''
    Download and install kubectl, the Kubernetes command-line tool. Download and install kubelogin, a client-go credential (exec) plugin implementing azure authentication.
    '''
    return call_az("az aks install-cli", locals())


def list(resource_group=None):
    '''
    List managed Kubernetes clusters.
    '''
    return call_az("az aks list", locals())


def remove_dev_spaces(name, resource_group, yes=None):
    '''
    Remove Azure Dev Spaces from a managed Kubernetes cluster.
    '''
    return call_az("az aks remove-dev-spaces", locals())


def scale(name, node_count, resource_group, no_wait=None, nodepool_name=None):
    '''
    Scale the node pool in a managed Kubernetes cluster.
    '''
    return call_az("az aks scale", locals())


def show(name, resource_group):
    '''
    Show the details for a managed Kubernetes cluster.
    '''
    return call_az("az aks show", locals())


def upgrade(name, resource_group, control_plane_only=None, kubernetes_version=None, no_wait=None, node_image_only=None, yes=None):
    '''
    Upgrade a managed Kubernetes cluster to a newer version.
    '''
    return call_az("az aks upgrade", locals())


def use_dev_spaces(name, resource_group, endpoint=None, space=None, update=None, yes=None):
    '''
    Use Azure Dev Spaces with a managed Kubernetes cluster.
    '''
    return call_az("az aks use-dev-spaces", locals())


def rotate_certs(name, resource_group, no_wait=None, yes=None):
    '''
    Rotate certificates and keys on a managed Kubernetes cluster
    '''
    return call_az("az aks rotate-certs", locals())


def wait(name, resource_group, created=None, custom=None, deleted=None, exists=None, interval=None, timeout=None, updated=None):
    '''
    Wait for a managed Kubernetes cluster to reach a desired state.
    '''
    return call_az("az aks wait", locals())


def stop(name, resource_group, no_wait=None):
    return call_az("az aks stop", locals())


def start(name, resource_group, no_wait=None):
    return call_az("az aks start", locals())


def get_versions(location):
    '''
    Get the versions available for creating a managed Kubernetes cluster.
    '''
    return call_az("az aks get-versions", locals())

