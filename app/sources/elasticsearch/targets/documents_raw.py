from datetime import datetime
import json
import os

from settings import ES_INDEX

# load categories map from a json
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'categories.json')) as f:
    categories = json.load(f)


def documents_raw(es, from_date, to_date, query_string):
    """ Returns the number of documents aggregated per category
        Adds a time coordinate, choosen in the middle of the considered
        range, because grafana likes to eat stuff which can be considered
        a timeseries
    """
    res = es.search(
        index=ES_INDEX,
        body={
            "size": 500,
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
            "sort": {
                "date": {
                    "order": "desc",
                    "unmapped_type": "boolean"
                }
            },
            "script_fields": {},
            "docvalue_fields": ["date"]
        })
    hits = res.get('hits').get('hits')
    rows = []
    for h in hits:
        s = h.get('_source')
        rows.append([
            s.get('url'),
            s.get('ft_title'),
            s.get('ft_body'),
            list(map(lambda ctg: categories.get(ctg), s.get('categories'))),
            s.get('language'),
            s.get('country').get('name'),
            h.get('fields').get('date')[0]
        ])
    return [{
        "columns": [{
            "text": "URL",
            "type": "link"
        }, {
            "text": "Title",
            "type": "string"
        }, {
            "text": "Body",
            "type": "string"
        }, {
            "text": "Categories",
            "type": "string"
        }, {
            "text": "Country",
            "type": "string"
        }, {
            "text": "Language",
            "type": "string"
        }, {
            "text": "Date",
            "type": "time"
        }],
        "rows": rows,
        "type": "table"
    }]
