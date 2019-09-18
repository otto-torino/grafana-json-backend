import json
import os

from settings import BUCKETS, ES_INDEX

# load categories map from a json
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'categories.json')) as f:
    categories = json.load(f)


def categories_timeline(es, from_date, to_date, interval, query_string):
    """ Returns the number of documents aggregated per category
        Adds a time coordinate, choosen in the middle of the considered
        range, because grafana likes to eat stuff which can be considered
        a timeseries
    """
    interval = round((to_date - from_date) / BUCKETS)
    res = es.search(
        index=ES_INDEX,
        body={
            "size": 0,
            "query": {
                "bool": {
                    "filter": [{
                        "range": {
                            "date": {
                                "gte": from_date,
                                "lte": to_date,
                                "format": "epoch_millis"
                            }
                        }
                    }, {
                        "query_string": query_string
                    }]
                }
            },
            "aggs": {
                "timeline": {
                    "date_histogram": {
                        "interval": interval,
                        "field": "date",
                        "min_doc_count": 1,
                        # "extended_bounds": {
                        #     "min": from_date,
                        #     "max": to_date
                        # },
                        "format": "epoch_millis"
                    },
                    "aggs": {
                        "cat": {
                            "terms": {
                                "field": "categories",
                                "size": 50,
                                "order": {
                                    "_count": "desc"
                                },
                                "min_doc_count": 1
                            }
                        }
                    }
                }
            }
        })
    cat = {}
    tot = []
    for b in res.get('aggregations').get('timeline').get('buckets'):
        tot.append([b.get('doc_count'), b.get('key')])
        for c in b.get('cat').get('buckets'):
            if cat.get(c.get('key')) is None:
                cat[c.get('key')] = []
            cat[c.get('key')].append([c.get('doc_count'), b.get('key')])
        result = [
            {
                'target': 'Documents',
                'datapoints': tot
            }
        ]
        for k, v in cat.items():
            result.append({
                'target': categories.get(k),
                'datapoints': v
            })
    return result
