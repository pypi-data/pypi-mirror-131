from .. pyaz_utils import call_az

def list():
    '''
    List registered clouds.
    '''
    return call_az("az cloud list", locals())


def show(name=None):
    '''
    Get the details of a registered cloud.
    '''
    return call_az("az cloud show", locals())


def register(name, cloud_config=None, endpoint_active_directory=None, endpoint_active_directory_data_lake_resource_id=None, endpoint_active_directory_graph_resource_id=None, endpoint_active_directory_resource_id=None, endpoint_gallery=None, endpoint_management=None, endpoint_resource_manager=None, endpoint_sql_management=None, endpoint_vm_image_alias_doc=None, profile=None, suffix_acr_login_server_endpoint=None, suffix_azure_datalake_analytics_catalog_and_job_endpoint=None, suffix_azure_datalake_store_file_system_endpoint=None, suffix_keyvault_dns=None, suffix_sql_server_hostname=None, suffix_storage_endpoint=None):
    '''
    Register a cloud.
    '''
    return call_az("az cloud register", locals())


def unregister(name):
    '''
    Unregister a cloud.
    '''
    return call_az("az cloud unregister", locals())


def set(name, profile=None):
    '''
    Set the active cloud.
    '''
    return call_az("az cloud set", locals())


def update(cloud_config=None, endpoint_active_directory=None, endpoint_active_directory_data_lake_resource_id=None, endpoint_active_directory_graph_resource_id=None, endpoint_active_directory_resource_id=None, endpoint_gallery=None, endpoint_management=None, endpoint_resource_manager=None, endpoint_sql_management=None, endpoint_vm_image_alias_doc=None, name=None, profile=None, suffix_acr_login_server_endpoint=None, suffix_azure_datalake_analytics_catalog_and_job_endpoint=None, suffix_azure_datalake_store_file_system_endpoint=None, suffix_keyvault_dns=None, suffix_sql_server_hostname=None, suffix_storage_endpoint=None):
    '''
    Update the configuration of a cloud.
    '''
    return call_az("az cloud update", locals())


def list_profiles(name=None, show_all=None):
    '''
    List the supported profiles for a cloud.
    '''
    return call_az("az cloud list-profiles", locals())

