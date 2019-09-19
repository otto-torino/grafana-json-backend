from settings import ES_INDEX


def location(es, from_date, to_date, interval, query_string):
    """ Returns the number of documents aggregated per location
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
            "aggs": {
                "countries": {
                    "terms": {
                        "field": "country.iso-a2",
                        "size": 10,
                        "order": {"_key": "desc"},
                        "min_doc_count": 1
                    },
                    "aggs": {
                        "timeline": {
                           "date_histogram": {
                               "interval": interval,
                               "field": "date",
                               "min_doc_count": 0,
                               # "extended_bounds": {"min": "1553014405322", "max":"1568908405322"},
                               "format": "epoch_millis"
                            }
                        }
                    }
                }
            }
        })
    time = int(from_date) + int((int(to_date) - int(from_date)) / 2)
    result = []
    for b in res.get('aggregations').get('countries').get('buckets'):
        result.append({
            'target': (b.get('key')),
            'datapoints': [[b.get('doc_count'), time]]
        })
    return result
