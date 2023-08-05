from .... pyaz_utils import call_az

def list(name, resource_group, slot=None):
    '''
    List the restorable snapshots for a web app.
    '''
    return call_az("az webapp config snapshot list", locals())


def restore(name, resource_group, time, restore_content_only=None, slot=None, source_name=None, source_resource_group=None, source_slot=None):
    '''
    Restore a web app snapshot.
    '''
    return call_az("az webapp config snapshot restore", locals())

