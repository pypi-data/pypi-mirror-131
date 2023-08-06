from .... pyaz_utils import _call_az

def show(name, resource_group, server):
    '''
    Show the current ledger digest settings.
    '''
    return _call_az("az sql db ledger-digest-uploads show", locals())


def enable(endpoint, name, resource_group, server):
    '''
    Enable uploading ledger digests to an Azure Storage account or to Azure Confidential Ledger. If uploading ledger digests is already enabled, the cmdlet resets the digest storage endpoint to a new value.
    '''
    return _call_az("az sql db ledger-digest-uploads enable", locals())


def disable(name, resource_group, server):
    '''
    Disable uploading ledger digests.
    '''
    return _call_az("az sql db ledger-digest-uploads disable", locals())

