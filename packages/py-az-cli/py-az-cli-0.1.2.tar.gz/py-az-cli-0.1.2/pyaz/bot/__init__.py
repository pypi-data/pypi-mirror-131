from .. pyaz_utils import call_az
from . import authsetting, directline, email, facebook, kik, msteams, skype, slack, sms, telegram, webchat


def create(appid, kind, name, resource_group, cmk_key_vault_key_url=None, description=None, display_name=None, echo=None, lang=None, location=None, sku=None, tags=None):
    '''
    Create a new v4 SDK bot.
    '''
    return call_az("az bot create", locals())


def publish(name, resource_group, code_dir=None, keep_node_modules=None, proj_file_path=None, timeout=None):
    '''
    Publish to a bot's associated app service.
    '''
    return call_az("az bot publish", locals())


def download(name, resource_group, save_path=None):
    '''
    Download an existing bot.
    '''
    return call_az("az bot download", locals())


def prepare_publish(name, proj_file_path, resource_group, sln_name, code_dir=None):
    '''
    (Maintenance mode) Add scripts to your local source code directory to be able to publish back using `az bot publish` for v3 SDK bots.
    '''
    return call_az("az bot prepare-publish", locals())


def prepare_deploy(lang, code_dir=None, proj_file_path=None):
    '''
    Add scripts/config files for publishing with `az webapp deployment`.
    '''
    return call_az("az bot prepare-deploy", locals())


def show(name, resource_group, msbot=None):
    '''
    Get an existing bot.
    '''
    return call_az("az bot show", locals())


def delete(name, resource_group):
    '''
    Delete an existing bot.
    '''
    return call_az("az bot delete", locals())


def update(name, resource_group, app_insights_api_key=None, app_insights_app_id=None, app_insights_key=None, cmk_key_vault_key_url=None, cmk_off=None, description=None, display_name=None, endpoint=None, icon_url=None, sku=None, tags=None):
    '''
    Update an existing bot.
    '''
    return call_az("az bot update", locals())

