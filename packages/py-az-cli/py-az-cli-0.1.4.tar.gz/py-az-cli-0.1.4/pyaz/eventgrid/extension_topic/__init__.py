from ... pyaz_utils import _call_az

def show(scope):
    '''
    Get the details of an extension topic.
    '''
    return _call_az("az eventgrid extension-topic show", locals())

