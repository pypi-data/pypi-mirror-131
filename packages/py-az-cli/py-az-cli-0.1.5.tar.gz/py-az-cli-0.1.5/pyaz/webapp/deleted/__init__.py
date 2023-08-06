from ... pyaz_utils import _call_az

def list(name=None, resource_group=None, slot=None):
    '''
    List web apps that have been deleted.
    '''
    return _call_az("az webapp deleted list", locals())


def restore(deleted_id, name, resource_group, restore_content_only=None, slot=None):
    '''
    Restore a deleted web app.
    '''
    return _call_az("az webapp deleted restore", locals())

