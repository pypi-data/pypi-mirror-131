from ... pyaz_utils import call_az

def init_recovery(sd_exchange_key, hsm_name=None, id=None):
    '''
    Retrieve the exchange key of the HSM.
    '''
    return call_az("az keyvault security-domain init-recovery", locals())


def upload(sd_exchange_key, sd_file, sd_wrapping_keys, hsm_name=None, id=None, no_wait=None, passwords=None):
    '''
    Start to restore the HSM.
    '''
    return call_az("az keyvault security-domain upload", locals())


def download(sd_quorum, sd_wrapping_keys, security_domain_file, hsm_name=None, id=None, no_wait=None):
    '''
    Download the security domain file from the HSM.
    '''
    return call_az("az keyvault security-domain download", locals())


def wait(hsm_name=None, id=None, target_operation=None):
    '''
    Place the CLI in a waiting state until HSM security domain operation is finished.
    '''
    return call_az("az keyvault security-domain wait", locals())

