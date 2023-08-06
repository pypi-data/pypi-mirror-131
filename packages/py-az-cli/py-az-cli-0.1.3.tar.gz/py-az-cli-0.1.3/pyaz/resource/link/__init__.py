from ... pyaz_utils import _call_az

def create(link, target, notes=None):
    '''
    Create a new link between resources.
    '''
    return _call_az("az resource link create", locals())


def delete(link):
    '''
    Delete a link between resources.
    '''
    return _call_az("az resource link delete", locals())


def show(link):
    return _call_az("az resource link show", locals())


def list(filter=None, scope=None):
    '''
    List resource links.
    '''
    return _call_az("az resource link list", locals())


def update(link, notes=None, target=None):
    '''
    Update link between resources.
    '''
    return _call_az("az resource link update", locals())

