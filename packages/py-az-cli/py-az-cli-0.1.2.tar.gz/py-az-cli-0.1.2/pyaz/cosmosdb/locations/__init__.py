from ... pyaz_utils import call_az

def show(location):
    '''
    Show the Azure CosmosDB location properties in the given location.
    '''
    return call_az("az cosmosdb locations show", locals())


def list():
    '''
    Retrieves the list of cosmosdb locations and their properties.
    '''
    return call_az("az cosmosdb locations list", locals())

