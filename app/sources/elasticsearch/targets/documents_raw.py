from datetime import datetime
from settings import ES_INDEX


def documents_raw(es, categories_dict, from_date, to_date, query_string):
    """ Returns all the documents
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
            list(map(lambda ctg: categories_dict.get(ctg), s.get('categories'))),
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
