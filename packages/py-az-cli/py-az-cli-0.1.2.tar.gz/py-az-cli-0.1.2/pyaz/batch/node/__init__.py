from ... pyaz_utils import call_az
from . import file, remote_desktop, remote_login_settings, scheduling, service_logs, user


def delete(pool_id, account_endpoint=None, account_key=None, account_name=None, if_match=None, if_modified_since=None, if_none_match=None, if_unmodified_since=None, json_file=None, node_deallocation_option=None, node_list=None, resize_timeout=None):
    return call_az("az batch node delete", locals())


def show(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, select=None):
    return call_az("az batch node show", locals())


def list(pool_id, account_endpoint=None, account_key=None, account_name=None, filter=None, select=None):
    return call_az("az batch node list", locals())


def reboot(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, node_reboot_option=None):
    return call_az("az batch node reboot", locals())


def reimage(node_id, pool_id, account_endpoint=None, account_key=None, account_name=None, node_reimage_option=None):
    return call_az("az batch node reimage", locals())

