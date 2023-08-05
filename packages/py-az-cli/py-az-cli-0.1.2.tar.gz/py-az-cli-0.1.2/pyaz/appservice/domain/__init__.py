from ... pyaz_utils import call_az

def create(contact_info, hostname, resource_group, accept_terms=None, auto_renew=None, dryrun=None, privacy=None, tags=None):
    '''
    Create and purchase a custom domain.
    '''
    return call_az("az appservice domain create", locals())


def show_terms(hostname):
    '''
    Show the legal terms for purchasing and creating a custom domain.
    '''
    return call_az("az appservice domain show-terms", locals())

