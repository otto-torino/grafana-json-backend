from settings import ES_INDEX


def documents_tot(es, from_date, to_date, query_string):
    """ Returns the total number of documents
    """
    res = es.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "date": {
                                    "gte": from_date,
                                    "lte": to_date,
                                    "format": "epoch_millis"
                                }
                            }
                        },
                        {
                            "query_string": query_string
                        }
                    ]
                }
            },
            "aggs": {}
        })
    print(res)
    time = int(from_date) + int((int(to_date) - int(from_date)) / 2)
    result = [{
        'target': 'documents',
        'datapoints': [[res.get('hits').get('total').get('value'), time]]
    }]
    return result
