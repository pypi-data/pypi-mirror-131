from .... pyaz_utils import call_az

def add(account_name, allowed_clients, cifs, nfsv3, nfsv41, pool_name, resource_group, rule_index, unix_read_only, unix_read_write, volume_name, add=None, force_string=None, remove=None, set=None):
    '''
    Add a new rule to the export policy for a volume.
    '''
    return call_az("az netappfiles volume export-policy add", locals())


def list(account_name, pool_name, resource_group, volume_name):
    '''
    List the export policy rules for a volume.
    '''
    return call_az("az netappfiles volume export-policy list", locals())


def remove(account_name, pool_name, resource_group, rule_index, volume_name, add=None, force_string=None, remove=None, set=None):
    '''
    Remove a rule from the export policy for a volume by rule index. The current rules can be obtained by performing the subgroup list command.
    '''
    return call_az("az netappfiles volume export-policy remove", locals())

