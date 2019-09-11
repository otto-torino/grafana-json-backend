import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'categories.json')) as f:
    categories = json.load(f)


def categories_cnt(es, from_date, to_date, query_string):
    res = es.search(
        index="osint",
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
                "cat": {
                    "terms": {
                        "field": "categories",
                        "size": 20,
                        "order": {
                            "_count": "desc"
                        },
                        "min_doc_count": 1
                    },
                    # the following not used because times are not aggregated, instead
                    # doc numbers are tied to the mean point of the time range
                    # "aggs": {
                    #     "2": {
                    #         "date_histogram": {
                    #             "interval": "1d",
                    #             "field": "date",
                    #             "min_doc_count": 1,
                    #             "extended_bounds": {
                    #                 "min": "1552299869071",
                    #                 "max": "1568193869071"
                    #             },
                    #             "format": "epoch_millis"
                    #         },
                    #         "aggs": {}
                    #     }
                    # }
                }
            }
        })
    time = int(from_date) + int((int(to_date) - int(from_date)) / 2)
    result = []
    for b in res.get('aggregations').get('cat').get('buckets'):
        result.append({
            'target': categories.get(b.get('key')),
            'datapoints': [[b.get('doc_count'), time]]
        })
    return result
