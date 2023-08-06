from .... pyaz_utils import _call_az

def show(resource_group, storage_account):
    '''
    Display Advanced Threat Protection settings for a storage account.
    '''
    return _call_az("az security atp storage show", locals())


def update(is_enabled, resource_group, storage_account):
    '''
    Toggle status of Advanced Threat Protection for a storage account.
    '''
    return _call_az("az security atp storage update", locals())

